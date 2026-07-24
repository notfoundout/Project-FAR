# Pinned SWE-bench TestSpec interface

The environment-preparation controller is locked to SWE-bench commit `f7bbbb2ccdf479001d6467c9e34af59e44a840f9`.

Required properties are `base_dockerfile`, `env_dockerfile`, `instance_dockerfile`, `setup_env_script`, `install_repo_script`, `eval_script`, `base_image_key`, `env_image_key`, `instance_image_key`, and `platform`.

`setup_repo_script` is not part of the pinned interface and must not be used.
