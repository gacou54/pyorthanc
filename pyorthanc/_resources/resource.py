import abc
from typing import Any, BinaryIO, Dict, List, Optional, Union

from httpx._types import QueryParamTypes

from .. import errors, util
from ..client import Orthanc


class Resource:

    def __init__(self, id_: str, client: Orthanc, _lock_children: bool = False) -> None:
        """Constructor

        Parameters
        ----------
        id_
            Orthanc identifier of the resource
        client
            Orthanc client
        _lock_children
            If `_lock_children` is True, the resource children (ex. instances of a series via `Series.instances`)
            will be cached at the first query rather than queried every time. This is useful when you want
            to filter the children of a resource and want to maintain the filter result.
        """
        client = util.ensure_non_raw_response(client)

        self.id_ = id_
        self.client = client

        self._lock_children = _lock_children
        self._main_dicom_tags: Optional[Dict] = None
        self._child_resources: Optional[List['Resource']] = None

    @property
    def identifier(self) -> str:
        """Get Orthanc's identifier

        Returns
        -------
        str
            Resource's identifier
        """
        return self.id_

    @property
    def main_dicom_tags(self) -> Dict[str, str]:
        if self._main_dicom_tags is None:
            self._main_dicom_tags = self.get_main_information()['MainDicomTags']

        return self._main_dicom_tags

    @abc.abstractmethod
    def legacy_viewer_url(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_main_information(self):
        raise NotImplementedError

    def _get_main_dicom_tag_value(self, tag: str) -> Any:
        try:
            return self.main_dicom_tags[tag]
        except KeyError:
            raise errors.TagDoesNotExistError(f'{self} has no {tag} tag.')

    def _make_response_format_params(self, simplify: bool = False, short: bool = False) -> Dict:
        if simplify and not short:
            params = {'simplify': True}
        elif short and not simplify:
            params = {'short': True}
        elif simplify and short:
            raise ValueError('simplify and short can\'t be both True.')
        else:
            params = {}

        return params

    def _download_file(
            self, url: str,
            filepath: Union[str, BinaryIO],
            with_progress: bool = False,
            params: Optional[QueryParamTypes] = None):
        # Check if filepath is a path or a file object.
        if isinstance(filepath, str):
            is_file_object = False
            filepath = open(filepath, 'wb')
        elif hasattr(filepath, 'write') and hasattr(filepath, 'seek'):
            is_file_object = True
        else:
            raise TypeError(f'"path" must be a file-like object or a file path, got "{type(filepath).__name__}".')

        try:
            with self.client.stream('GET', url, params=params) as response:
                if with_progress:
                    try:
                        from tqdm import tqdm
                    except ModuleNotFoundError:
                        raise ModuleNotFoundError(
                            'Optional dependency tqdm have to be installed for the progress indicator. '
                            'Install with `pip install pyorthanc[progress]` or `pip install pyorthanc[all]'
                        )

                    last_num_bytes_downloaded = response.num_bytes_downloaded

                    with tqdm(unit='B', unit_scale=True, desc=self.__repr__()) as progress:
                        for chunk in response.iter_bytes():
                            filepath.write(chunk)
                            progress.update(response.num_bytes_downloaded - last_num_bytes_downloaded)
                            last_num_bytes_downloaded = response.num_bytes_downloaded

                else:
                    for chunk in response.iter_bytes():
                        filepath.write(chunk)

        finally:
            if not is_file_object:
                filepath.close()

    def __eq__(self, other: 'Resource') -> bool:
        return self.id_ == other.id_

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id_})'
