"""Checks for gee:status validity.

gee:status specifies whether a dataset is not completely active.

Requirements and specification:
- If the node is a catalog, it cannot have the field.
- If the field is set, its value must be one of several enum values.
"""

from typing import Iterator

from checker import stac
from stac import stac_lib


class Check(stac.NodeCheck):
  """Checks for gee:status."""
  name = 'gee_status'

  @classmethod
  def run(cls, node: stac.Node) -> Iterator[stac.Issue]:
    if stac_lib.GEE_STATUS in node.stac:
      if node.type == stac.StacType.CATALOG:
        yield cls.new_issue(
            node, f'Catalogs may not have a {stac_lib.GEE_STATUS} field'
        )
      elif node.type == stac.StacType.COLLECTION:
        field_value = node.stac.get(stac_lib.GEE_STATUS)
        if field_value not in stac_lib.Status.allowed_statuses():
          yield cls.new_issue(
              node,
              f'{stac_lib.GEE_STATUS}, if set, must be one of'
              f' {sorted(stac_lib.Status.allowed_statuses())}',
          )
