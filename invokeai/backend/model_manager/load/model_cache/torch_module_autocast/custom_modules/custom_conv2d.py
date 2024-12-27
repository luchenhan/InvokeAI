import torch

from invokeai.backend.model_manager.load.model_cache.torch_module_autocast.cast_to_device import cast_to_device
from invokeai.backend.model_manager.load.model_cache.torch_module_autocast.custom_modules.custom_module_mixin import (
    CustomModuleMixin,
)
from invokeai.backend.model_manager.load.model_cache.torch_module_autocast.custom_modules.utils import (
    add_nullable_tensors,
)


class CustomConv2d(torch.nn.Conv2d, CustomModuleMixin):
    def _autocast_forward_with_patches(self, input: torch.Tensor) -> torch.Tensor:
        aggregated_param_residuals = self._aggregate_patch_parameters(self._patches_and_weights)
        weight = add_nullable_tensors(self.weight, aggregated_param_residuals["weight"])
        bias = add_nullable_tensors(self.bias, aggregated_param_residuals["bias"])
        return torch.nn.functional.conv2d(input, weight, bias)

    def _autocast_forward(self, input: torch.Tensor) -> torch.Tensor:
        weight = cast_to_device(self.weight, input.device)
        bias = cast_to_device(self.bias, input.device)
        return self._conv_forward(input, weight, bias)

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        if len(self._patches_and_weights) > 0:
            return self._autocast_forward_with_patches(input)
        elif self._device_autocasting_enabled:
            return self._autocast_forward(input)
        else:
            return super().forward(input)
