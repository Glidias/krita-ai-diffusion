import ai_diffusion.ui.param_extensions as TOOLS
from .custom_workflow import register_param_extension, ParamKind

# Register
register_param_extension(ParamKind.text, "points_editor", TOOLS.open_points_editor)
register_param_extension(ParamKind.number_int, "random_seed", TOOLS.pick_random_seed)
register_param_extension(ParamKind.number_int, "pick_color", TOOLS.pick_color_as_int)
register_param_extension(ParamKind.number_int, "krita_fg_color", TOOLS.get_krita_foreground_color_as_int)
