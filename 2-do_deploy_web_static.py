#!/usr/bin/python3
"""
Fabric script that distributes an archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['54.83.110.209', '184.72.84.8']


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        folder_name = file_name.split(".")[0]
        release_path = "/data/web_static/releases/{}".format(folder_name)

        # Upload archive
        put(archive_path, "/tmp/{}".format(file_name))

        # Create release directory
        run("mkdir -p {}".format(release_path))

        # Uncompress the archive to the release folder
        run("tar -xzf /tmp/{} -C {}".format(file_name, release_path))

        # Remove archive
        run("rm /tmp/{}".format(file_name))

        # Move contents from web_static to release root
        run("mv {0}/web_static/* {0}/".format(release_path))

        # Remove now empty web_static dir
        run("rm -rf {}/web_static".format(release_path))

        # Remove current symlink and link to new release
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))

        return True
    except Exception as e:
        print("Error during deployment:", e)
        return False
