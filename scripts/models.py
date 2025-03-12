class SavedPrompt:
    def __init__(self, id_, name, positive_prompt, negative_prompt, image_path,
                 usage_count, is_favourite, created_at, is_removed, sampling_method,
                 sampling_steps, width, height, cfg_steps, clip_skip):
        self.id_ = id_
        self.name = name
        self.positive_prompt = positive_prompt
        self.negative_prompt = negative_prompt
        self.image_path = image_path
        self.usage_count = usage_count
        self.is_favourite = is_favourite
        self.created_at = created_at
        self.is_removed = is_removed
        self.sampler = sampling_method
        self.sampling_steps = sampling_steps
        self.width = width
        self.height = height
        self.cfg_scale = cfg_steps
        self.clip_skip = clip_skip

    def __str__(self):
        return (f"SavedPrompt:\n"
                f"  id_: {self.id_}\n"
                f"  name: {self.name}\n"
                f"  positive_prompt: {self.positive_prompt}\n"
                f"  negative_prompt: {self.negative_prompt}\n"
                f"  image_path: {self.image_path}\n"
                f"  usage_count: {self.usage_count}\n"
                f"  is_favourite: {self.is_favourite}\n"
                f"  created_at: {self.created_at}\n"
                f"  is_removed: {self.is_removed}\n"
                f"  sampling_method: {self.sampler}\n"
                f"  sampling_steps: {self.sampling_steps}\n"
                f"  width: {self.width}\n"
                f"  height: {self.height}\n"
                f"  cfg_steps: {self.cfg_scale}\n"
                f"  clip_skip: {self.clip_skip}")
