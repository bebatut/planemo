
``serve`` command
======================================

This section is auto-generated from the help text for the planemo command
``serve``. This help message can be generated with ``planemo serve
--help``.

**Usage**::

    planemo serve [OPTIONS] TOOL_PATH

**Help**

Launch Galaxy instance with specified tools.

The Galaxy tool panel will include just the referenced tool or tools (by
default all the tools in the current working directory) and the upload
tool.

planemo will search parent directories to see if any is a Galaxy instance
- but one can pick the Galaxy instance to use with the ``--galaxy_root``
option or force planemo to download a disposable instance with the
``--install_galaxy`` flag.

``planemo`` will run the Galaxy instance in an existing virtualenv if one
exists in a ``.venv`` directory in the specified ``--galaxy_root``.
Otherwise, the Galaxy instance will run in a clean virtualenv created in
``/tmp``.

``planemo`` uses temporarily generated config files and environment
variables to attempt to shield this execution of Galaxy from manually
launched runs against that same Galaxy root - but this may not be bullet
proof yet, so please be careful and do not try this against a production
Galaxy instance.

**Options**::


      --galaxy_root DIRECTORY         Root of development galaxy directory to
                                      execute command with.
      --galaxy_database_seed PATH     Preseeded Galaxy sqlite database to target.
      --extra_tools PATH              Extra tool sources to include in Galaxy's tool
                                      panel (file or directory). These will not be
                                      linted/tested/etc... but they will be
                                      available to workflows and for interactive
                                      use.
      --install_galaxy                Download and configure a disposable copy of
                                      Galaxy from github.
      --galaxy_branch TEXT            Branch of Galaxy to target (defaults to
                                      master) if a Galaxy root isn't specified.
      --galaxy_source TEXT            Git source of Galaxy to target (defaults to
                                      the official galaxyproject github source if a
                                      Galaxy root isn't specified.
      --skip_venv                     Do not create or source a virtualenv
                                      environment for Galaxy, this should be used or
                                      instance to preserve an externally configured
                                      virtual environment or conda environment.
      --no_cache_galaxy               Skip caching of Galaxy source and dependencies
                                      obtained with --install_galaxy. Not caching
                                      this results in faster downloads (no git) - so
                                      is better on throw away instances such with
                                      TravisCI.
      --no_cleanup                    Do not cleanup temp files created for and by
                                      Galaxy.
      --galaxy_email TEXT             E-mail address to use when launching single-
                                      user Galaxy server.
      --docker / --no_docker          Run Galaxy tools in Docker if enabled.
      --docker_cmd TEXT               Command used to launch docker (defaults to
                                      docker).
      --docker_sudo / --no_docker_sudo
                                      Flag to use sudo when running docker.
      --docker_host TEXT              Docker host to target when executing docker
                                      commands (defaults to localhost).
      --docker_sudo_cmd TEXT          sudo command to use when --docker_sudo is
                                      enabled (defaults to sudo).
      --mulled_containers, --biocontainers
                                      Test tools against mulled containers (forces
                                      --docker).
      --job_config_file PATH          Job configuration file for Galaxy to target.
      --tool_dependency_dir DIRECTORY
                                      Tool dependency dir for Galaxy to target.
      --port INTEGER                  Port to serve Galaxy on (default is 9090).
      --host TEXT                     Host to bind Galaxy to. Default is 127.0.0.1
                                      that is restricted to localhost connections
                                      for security reasons set to 0.0.0.0 to bind
                                      Galaxy to all ports including potentially
                                      publicly accessible ones.
      --engine [galaxy|docker_galaxy]
                                      Select an engine to serve aritfacts such as
                                      tools and workflows. Defaults to a local
                                      Galaxy, but running Galaxy within a Docker
                                      container.
      --non_strict_cwl                Disable strict validation of CWL.
      --docker_galaxy_image TEXT      Docker image identifier for docker-galaxy-
                                      flavor used if engine type is specified as
                                      ``docker-galaxy``. Defaults to to bgruening
                                      /galaxy-stable.
      --test_data DIRECTORY           test-data directory to for specified tool(s).
      --tool_data_table PATH          tool_data_table_conf.xml file to for specified
                                      tool(s).
      --dependency_resolvers_config_file PATH
                                      Dependency resolver configuration for Galaxy
                                      to target.
      --brew_dependency_resolution    Configure Galaxy to use plain brew dependency
                                      resolution.
      --shed_dependency_resolution    Configure Galaxy to use brewed Tool Shed
                                      dependency resolution.
      --no_dependency_resolution      Configure Galaxy with no dependency resolvers.
      --conda_prefix DIRECTORY        Conda prefix to use for conda dependency
                                      commands.
      --conda_exec PATH               Location of conda executable.
      --conda_debug                   Enable more verbose conda logging.
      --conda_channels, --conda_ensure_channels TEXT
                                      Ensure conda is configured with specified
                                      comma separated list of channels.
      --conda_use_local               Use locally built packages while building
                                      Conda environments.
      --conda_dependency_resolution   Configure Galaxy to use only conda for
                                      dependency resolution.
      --conda_copy_dependencies       Conda dependency resolution for Galaxy will
                                      copy dependencies instead of attempting to
                                      link them.
      --conda_auto_install / --no_conda_auto_install
                                      Conda dependency resolution for Galaxy will
                                      auto install will attempt to install requested
                                      but missing packages.
      --conda_auto_init / --no_conda_auto_init
                                      Conda dependency resolution for Galaxy will
                                      auto install conda itself using miniconda if
                                      not availabe on conda_prefix.
      --profile TEXT                  Location of pid file is executed with
                                      --daemon.
      --postgres                      Use postgres database type.
      --database_type [postgres|sqlite]
                                      Type of database to use for profile -
                                      currently only 'postgres' is available.
      --postgres_psql_path TEXT       Name or or path to postgres client binary
                                      (psql).
      --postgres_database_user TEXT   Postgres username for managed development
                                      databases.
      --postgres_database_host TEXT   Postgres host name for managed development
                                      databases.
      --postgres_database_port TEXT   Postgres port for managed development
                                      databases.
      --file_path DIRECTORY           Location for files created by Galaxy (e.g.
                                      database/files).
      --database_connection TEXT      Database connection string to use for Galaxy.
      --shed_tool_conf TEXT           Location of shed tools conf file for Galaxy.
      --shed_tool_path TEXT           Location of shed tools directory for Galaxy.
      --daemon                        Serve Galaxy process as a daemon.
      --pid_file TEXT                 Location of pid file is executed with
                                      --daemon.
      --cwl                           Configure Galaxy for use with CWL tool. (this
                                      option is experimental and will be replaced
                                      when and if CWL support is merged into
                                      Galaxy).
      --cwl_galaxy_root DIRECTORY     Root of development galaxy directory to
                                      execute command with (must be branch of Galaxy
                                      with CWL support, this option is experimental
                                      and will be replaced with --galaxy_root when
                                      and if CWL support is merged into Galaxy.
      --help                          Show this message and exit.
    
