import { Menu, MenuList } from '@invoke-ai/ui-library';
import { CanvasEntityActionMenuItems } from 'features/controlLayers/components/common/CanvasEntityActionMenuItems';
import { CanvasEntityMenuButton } from 'features/controlLayers/components/common/CanvasEntityMenuButton';
import { memo } from 'react';

export const ControlAdapterActionsMenu = memo(() => {
  return (
    <Menu>
      <CanvasEntityMenuButton />
      <MenuList>
        <CanvasEntityActionMenuItems />
      </MenuList>
    </Menu>
  );
});

ControlAdapterActionsMenu.displayName = 'ControlAdapterActionsMenu';