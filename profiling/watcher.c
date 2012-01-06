#include <errno.h>
#include <sys/fanotify.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include <linux/fcntl.h>

char* procfs;

void print_filename(int fd)
{
    char fd_path[1024], path[1024];
    int path_len;

    sprintf(fd_path, "%s/self/fd/%d", procfs, fd);
    path_len = readlink(fd_path, path, sizeof(path)-1);
    if (path_len < 0)
    {
        puts(fd_path);
        puts(": ");
        puts(strerror(errno));
    }
    else
    {
        path[path_len] = 0;
        puts(path);
    };
}

int main(int argc, char** argv) {
	int fan_fd, len;
	char buf[sizeof(struct fanotify_event_metadata)*1024];
	struct fanotify_event_metadata *metadata;
        
	if (argc != 3) {
		printf("Usage: %s <root-dir> <procfs>\n", argv[0]);
		return 1;
	}
        procfs = argv[2];

        fan_fd = fanotify_init(0, 0);
	if (fan_fd == -1) {
		perror("fanotify_init");
		return 1;
	}

        fanotify_mark(fan_fd, FAN_MARK_ADD | FAN_MARK_MOUNT, FAN_ACCESS, AT_FDCWD, argv[1]);
        if (fan_fd == -1) {
		perror("fanotify_mark");
                return 1;
        }
	while (1) {
		len = read(fan_fd, buf, sizeof(buf));
		metadata = (struct fanotify_event_metadata*)&buf;
		while (FAN_EVENT_OK(metadata, len)) {
			print_filename(metadata->fd);
			close(metadata->fd);
			metadata = FAN_EVENT_NEXT(metadata, len);
		}
	}
}
