# Comprehensive Linux Commands Guide

A detailed reference guide covering essential Linux commands with real-world use cases and practical explanations for developers, system administrators, and DevOps engineers.

**Table of Contents**

1. [File and Directory Management](#file-and-directory-management)
1. [File Viewing and Manipulation](#file-viewing-and-manipulation)
1. [User and Permission Management](#user-and-permission-management)
1. [Process Management](#process-management)
1. [Networking Commands](#networking-commands)
1. [System Information](#system-information)
1. [Text Processing and Searching](#text-processing-and-searching)
1. [Package Management](#package-management)
1. [Compression and Archiving](#compression-and-archiving)
1. [Advanced System Administration](#advanced-system-administration)

-----

## File and Directory Management

### `ls` - List Directory Contents

**Purpose**: Display files and directories in a directory.

```bash
ls                          # List files in current directory
ls -l                       # Long format (detailed information)
ls -a                       # Include hidden files (starting with .)
ls -lah                     # Long format, all files, human-readable sizes
ls -R                       # Recursive listing (subdirectories)
ls -lt                      # Sort by modification time
ls -lS                      # Sort by file size
ls /path/to/dir             # List specific directory
ls *.txt                    # List files matching pattern
```

**Use Cases**:

- **Audit file structure**: `ls -la /var/log` - Check all log files and permissions
- **Find large files**: `ls -lS | head -10` - Identify top 10 largest files
- **Development**: `ls -la` before committing to ensure no unwanted files are staged

**Real-world Example**:

```bash
# Check what changed in current directory
ls -lt | head -5           # Five most recently modified items
```

-----

### `cd` - Change Directory

**Purpose**: Navigate between directories in the filesystem.

```bash
cd /path/to/directory       # Absolute path
cd relative/path            # Relative path
cd ..                       # Parent directory
cd ~                        # Home directory
cd -                        # Previous directory
cd /                        # Root directory
```

**Use Cases**:

- **Project switching**: `cd ~/projects/my-app` - Navigate to project folder
- **Quick navigation**: `cd -` - Jump back to previous working directory
- **Root access**: `cd /` then `cd etc` - Navigate to system configuration

**Real-world Example**:

```bash
# When working with multiple projects
cd ~/frontend && npm run build
cd - && cd ~/backend && npm test
```

-----

### `pwd` - Print Working Directory

**Purpose**: Display the current directory path.

```bash
pwd                         # Show current path
pwd -L                      # Show logical path (with symbolic links)
pwd -P                      # Show physical path (resolved symbolic links)
```

**Use Cases**:

- **Script debugging**: Confirm location in shell scripts
- **Documentation**: Know exact path for configuration files
- **SSH sessions**: Verify you’re in correct location on remote server

**Real-world Example**:

```bash
# In shell script to ensure correct context
echo "Working directory: $(pwd)"
if [ "$(pwd)" != "$EXPECTED_DIR" ]; then
    echo "Error: Wrong directory"
    exit 1
fi
```

-----

### `mkdir` - Make Directory

**Purpose**: Create new directories.

```bash
mkdir new_dir               # Create single directory
mkdir -p path/to/nested/dir # Create parent directories as needed
mkdir dir1 dir2 dir3        # Create multiple directories
mkdir -m 755 secure_dir     # Create with specific permissions
```

**Use Cases**:

- **Project setup**: `mkdir -p src/{components,utils,services}` - Create project structure
- **Log organization**: `mkdir -p logs/{debug,error,info}` - Organize log directories
- **Backup structure**: `mkdir -p backup/{daily,weekly,monthly}` - Create backup schedule

**Real-world Example**:

```bash
# Initialize project structure
mkdir -p {src,tests,docs,config}/{js,css}
mkdir -p public/{images,fonts,downloads}
```

-----

### `cp` - Copy Files and Directories

**Purpose**: Copy files and directories.

```bash
cp source.txt dest.txt      # Copy file
cp -r source_dir dest_dir   # Copy directory recursively
cp -v source.txt dest.txt   # Verbose (show what's copying)
cp -p source.txt dest.txt   # Preserve permissions and timestamps
cp -i source.txt dest.txt   # Interactive (ask before overwrite)
cp source*.txt /dest/       # Copy multiple files matching pattern
```

**Use Cases**:

- **Backup before edit**: `cp config.yml config.yml.bak` - Safety backup
- **Deploy config**: `cp -r config/* /etc/myapp/` - Copy configuration files
- **Development**: `cp -r node_modules backup/` - Backup dependencies

**Real-world Example**:

```bash
# Backup database before migration
cp -p production.db production.db.backup.$(date +%Y%m%d)

# Copy entire project structure
cp -r ~/dev/old-project ~/dev/new-project
```

-----

### `mv` - Move or Rename Files

**Purpose**: Move or rename files and directories.

```bash
mv old_name.txt new_name.txt # Rename file
mv source.txt /dest/         # Move file to directory
mv -i source.txt dest.txt    # Interactive (ask before overwrite)
mv -v source.txt /dest/      # Verbose output
mv dir1 dir2                 # Rename directory
```

**Use Cases**:

- **Organize files**: `mv *.log /var/log/archive/` - Archive old logs
- **Rename logs**: `mv app.log app.log.1` - Rotate log files
- **Project rename**: `mv old-name new-name` - Rename entire project folder

**Real-world Example**:

```bash
# Log rotation pattern
mv access.log access.log.$(date +%Y%m%d)
gzip access.log.*

# Reorganize downloaded files
mv ~/Downloads/*.pdf ~/Documents/PDFs/
```

-----

### `rm` - Remove Files and Directories

**Purpose**: Delete files and directories permanently.

```bash
rm file.txt                 # Delete file
rm -f file.txt              # Force delete (no prompt)
rm -i file.txt              # Interactive (ask confirmation)
rm -r directory/            # Delete directory and contents
rm -rf directory/           # Force delete directory (use carefully!)
rm *.log                    # Delete files matching pattern
rm -v file.txt              # Verbose (show what's deleting)
```

**⚠️ CAUTION**: `rm -rf /` is catastrophic. Always double-check patterns.

**Use Cases**:

- **Clean build artifacts**: `rm -rf build/ dist/` - Remove compiled files
- **Remove logs**: `rm -f *.log` - Clean up old logs
- **Development cleanup**: `rm -rf node_modules package-lock.json` - Fresh install

**Real-world Example**:

```bash
# Safe deletion with confirmation
rm -i old_config_*.txt

# Clean up with confirmation
rm -rf build/ && echo "Build cleaned"
```

-----

### `touch` - Create or Update File

**Purpose**: Create empty files or update modification timestamp.

```bash
touch file.txt              # Create empty file
touch file1.txt file2.txt   # Create multiple files
touch -t 202301011200 file.txt # Set specific timestamp
touch -d "2023-01-01" file.txt # Set date
```

**Use Cases**:

- **Create placeholder files**: `touch index.html style.css script.js` - Start web project
- **Trigger builds**: Update file timestamp to trigger watches
- **Test purposes**: Create test files with specific timestamps

**Real-world Example**:

```bash
# Create .gitkeep to maintain empty directories
touch .gitkeep

# Create placeholder files for new feature
touch src/components/{Header,Footer,Sidebar}.jsx
```

-----

## File Viewing and Manipulation

### `cat` - Concatenate and Display Files

**Purpose**: Display file contents or concatenate multiple files.

```bash
cat file.txt                # Display file contents
cat file1.txt file2.txt     # Concatenate multiple files
cat file.txt | less         # Paginate through content
cat > file.txt              # Create file with keyboard input
cat file.txt > copy.txt     # Redirect output to new file
cat >> file.txt             # Append to file
cat << EOF > file.txt       # Here-document input
data here
EOF
```

**Use Cases**:

- **View logs**: `cat /var/log/syslog` - Check system logs
- **Read config**: `cat /etc/nginx/nginx.conf` - View configuration
- **Merge files**: `cat part1.sql part2.sql > full.sql` - Combine SQL files

**Real-world Example**:

```bash
# Create application config file
cat > config.json << EOF
{
  "environment": "production",
  "debug": false,
  "port": 8080
}
EOF

# Check entire error log
cat /var/log/app/error.log
```

-----

### `less` - View File Contents Interactively

**Purpose**: View large files with navigation capabilities.

```bash
less file.txt               # Open file for viewing
less +G file.txt            # Jump to end of file
less +/pattern file.txt     # Jump to first occurrence of pattern
```

**Navigation Keys**:

- `Space` or `Page Down` - Next page
- `b` or `Page Up` - Previous page
- `g` - Beginning of file
- `G` - End of file
- `/pattern` - Search forward
- `?pattern` - Search backward
- `n` - Next match
- `N` - Previous match
- `q` - Quit

**Use Cases**:

- **Browse large logs**: `less /var/log/syslog` - Navigate through system logs
- **Code review**: `less src/main.py` - Review large source files
- **Configuration review**: `less /etc/nginx/nginx.conf`

**Real-world Example**:

```bash
# Search for errors in large log file
less +/ERROR /var/log/application.log
# Then use 'n' to find next occurrence
```

-----

### `tail` - Display End of File

**Purpose**: Show the last lines of a file or monitor live updates.

```bash
tail file.txt               # Show last 10 lines
tail -n 20 file.txt         # Show last 20 lines
tail -f file.txt            # Follow file (watch updates in real-time)
tail -F file.txt            # Follow with file rotation support
tail -c 100 file.txt        # Show last 100 bytes
tail -f file.txt | grep ERROR # Monitor specific lines
```

**Use Cases**:

- **Monitor logs**: `tail -f /var/log/app.log` - Watch application logs in real-time
- **Debug deployment**: `tail -F deploy.log` - Follow deployment output
- **Check recent errors**: `tail -n 50 error.log | grep CRITICAL`

**Real-world Example**:

```bash
# Monitor multiple log files
tail -f /var/log/app.log /var/log/error.log

# Follow application startup
docker logs -f container_name

# Monitor with pattern matching
tail -f /var/log/nginx/access.log | grep 404
```

-----

### `head` - Display Beginning of File

**Purpose**: Show the first lines of a file.

```bash
head file.txt               # Show first 10 lines
head -n 20 file.txt         # Show first 20 lines
head -c 100 file.txt        # Show first 100 bytes
head -n 5 file.txt | tail -n 2 # Get lines 4-5
```

**Use Cases**:

- **Check file format**: `head data.csv` - Verify CSV structure
- **Quick review**: `head config.yml` - Check configuration start
- **Extract subset**: `head -n 100 large_file.txt` - Sample from large file

**Real-world Example**:

```bash
# Check CSV header before processing
head -n 1 data.csv

# Combine with other commands
head -n 5 error.log | tail -n 2
```

-----

### `grep` - Search Text Pattern

**Purpose**: Search for text patterns in files.

```bash
grep "pattern" file.txt     # Search for pattern
grep -i "pattern" file.txt  # Case-insensitive search
grep -r "pattern" dir/      # Recursive search in directory
grep -n "pattern" file.txt  # Show line numbers
grep -c "pattern" file.txt  # Count matches
grep -v "pattern" file.txt  # Invert match (exclude pattern)
grep -E "regex" file.txt    # Use extended regex
grep -o "pattern" file.txt  # Show only matched parts
```

**Use Cases**:

- **Find errors**: `grep ERROR app.log` - Extract error lines
- **Search codebase**: `grep -r "function_name" src/` - Find function definitions
- **Configuration check**: `grep "port" /etc/nginx/nginx.conf` - Find config values
- **Log analysis**: `grep -c "404" access.log` - Count 404 errors

**Real-world Example**:

```bash
# Find all TODO comments in code
grep -r "TODO:" src/ --include="*.js"

# Extract specific user from logs
grep "username" /var/log/auth.log

# Find configuration issues
grep -i "error\|warning" config.log

# Count specific events
grep -c "user login" /var/log/syslog
```

-----

### `sed` - Stream Editor

**Purpose**: Perform text transformations on streams.

```bash
sed 's/old/new/' file.txt   # Replace first occurrence per line
sed 's/old/new/g' file.txt  # Replace all occurrences
sed -i 's/old/new/g' file.txt # Edit file in-place
sed '5d' file.txt           # Delete line 5
sed '1,5d' file.txt         # Delete lines 1-5
sed -n '5p' file.txt        # Print only line 5
sed -e 's/a/b/g' -e 's/c/d/g' file.txt # Multiple operations
```

**Use Cases**:

- **Configuration update**: `sed -i 's/localhost/example.com/g' config.txt`
- **Remove lines**: `sed -i '/^#/d' config.txt` - Remove comments
- **Format conversion**: `sed 's/,/\t/g' data.csv > data.tsv` - CSV to TSV
- **Environment replacement**: `sed "s|\${ENV}|production|g" template.conf`

**Real-world Example**:

```bash
# Update database connection string
sed -i "s/localhost:5432/$DB_HOST:$DB_PORT/g" config.ini

# Remove commented lines from config
sed -i '/^[[:space:]]*#/d; /^[[:space:]]*$/d' nginx.conf

# Batch rename files
for file in *.txt; do
    sed -i 's/old_pattern/new_pattern/g' "$file"
done
```

-----

### `awk` - Text Processing Language

**Purpose**: Process and extract data from structured text.

```bash
awk '{print $1}' file.txt   # Print first column
awk '{print $1, $3}' file.txt # Print first and third columns
awk -F: '{print $1}' /etc/passwd # Use different delimiter
awk '{sum += $1} END {print sum}' numbers.txt # Sum values
awk 'NR > 1' file.txt       # Skip header line
awk '$2 > 100' file.txt     # Filter rows where column 2 > 100
```

**Variables**:

- `NR` - Number of records (lines)
- `NF` - Number of fields
- `FS` - Field separator
- `OFS` - Output field separator
- `$0` - Entire line
- `$1, $2, ...` - Specific fields

**Use Cases**:

- **Extract data**: `awk '{print $1}' access.log | sort | uniq -c` - Top IPs
- **Parse CSV**: `awk -F, '{print $2}' data.csv` - Extract column from CSV
- **Calculate stats**: `awk '{sum += $1; count++} END {print sum/count}' data.txt` - Average
- **System info**: `awk -F: '{print $1}' /etc/passwd` - List all users

**Real-world Example**:

```bash
# Extract top 5 most common IPs from access logs
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -5

# Parse and format output
awk -F, '{printf "%-20s %s\n", $1, $3}' data.csv

# Calculate average response time
awk '{sum += $NF; count++} END {print "Average:", sum/count}' times.log

# Extract specific columns and filter
awk -F: '$3 > 1000 {print $1, $3}' /etc/passwd
```

-----

## User and Permission Management

### `sudo` - Execute as Superuser

**Purpose**: Run commands with superuser privileges.

```bash
sudo command                # Run command as root
sudo -u username command    # Run as specific user
sudo -i                     # Start interactive root shell
sudo -s                     # Start shell as root
sudo -l                     # List allowed commands
sudo !!                     # Repeat last command with sudo
```

**Use Cases**:

- **System updates**: `sudo apt-get update && sudo apt-get upgrade`
- **File ownership**: `sudo chown user:group file.txt`
- **Package installation**: `sudo npm install -g package-name`
- **Port binding**: `sudo netstat -tulpn` - Check ports

**Real-world Example**:

```bash
# Install software globally
sudo npm install -g typescript

# Fix file permissions
sudo chown -R appuser:appgroup /var/www/app

# Restart services
sudo systemctl restart nginx
```

-----

### `chmod` - Change File Permissions

**Purpose**: Modify file and directory permissions.

```bash
chmod 755 file.txt          # Set specific permissions
chmod u+x file.sh           # Add execute permission for owner
chmod g+r file.txt          # Add read for group
chmod o-w file.txt          # Remove write from others
chmod -R 755 directory/     # Recursive change
chmod a+x script.sh         # Add execute for all
```

**Permission Values**:

- `r` (read) = 4
- `w` (write) = 2
- `x` (execute) = 1

**Common Patterns**:

- `755` - rwxr-xr-x (owner full, others read/execute)
- `644` - rw-r–r– (owner write, others read)
- `700` - rwx—— (owner only)

**Use Cases**:

- **Make script executable**: `chmod +x deploy.sh`
- **Secure private files**: `chmod 600 private_key`
- **Web content**: `chmod 644 index.html && chmod 755 public/`
- **Database socket**: `chmod 660 db.socket`

**Real-world Example**:

```bash
# Set proper permissions for web application
chmod 755 /var/www/app
chmod 644 /var/www/app/config.ini
chmod 755 /var/www/app/scripts/deploy.sh

# Secure SSH keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/authorized_keys
```

-----

### `chown` - Change File Ownership

**Purpose**: Change file owner and group.

```bash
chown user file.txt         # Change owner
chown user:group file.txt   # Change owner and group
chown -R user:group dir/    # Recursive change
chown :group file.txt       # Change group only
```

**Use Cases**:

- **Deploy applications**: `sudo chown -R appuser:appgroup /var/www/app`
- **Fix permissions**: `sudo chown root:root /etc/config.conf`
- **Transfer ownership**: `chown newuser:newgroup /home/newuser`

**Real-world Example**:

```bash
# Set up application directory
sudo chown -R appuser:appgroup /opt/myapp
sudo chown -R www-data:www-data /var/www/html

# Change database file owner
sudo chown mysql:mysql /var/lib/mysql/database.db
```

-----

### `whoami` - Current User

**Purpose**: Display current user identity.

```bash
whoami                      # Show current username
id                          # Show user ID and groups
id -u                       # Show only user ID
id -g                       # Show only group ID
groups                      # Show all groups for current user
```

**Use Cases**:

- **Debug permissions**: Verify running user in scripts
- **Security audit**: Check process permissions
- **Script validation**: Ensure script runs as correct user

**Real-world Example**:

```bash
# In shell script
if [ "$(whoami)" != "root" ]; then
    echo "This script requires root privileges"
    exit 1
fi

# Check user in cron job
echo "Running as: $(whoami)" >> cron.log
```

-----

### `passwd` - Change Password

**Purpose**: Change user password.

```bash
passwd                      # Change current user password
passwd username             # Change other user password (root only)
passwd -l username          # Lock user account
passwd -u username          # Unlock user account
passwd -e username          # Expire password (force change on login)
```

**Use Cases**:

- **User management**: `sudo passwd newuser` - Set password for new user
- **Security**: `passwd -l compromised_user` - Disable account
- **Maintenance**: `passwd -e user` - Force password change

**Real-world Example**:

```bash
# Create new user and set password
sudo useradd -m -s /bin/bash newuser
sudo passwd newuser

# Disable inactive account
sudo passwd -l inactiveuser
```

-----

## Process Management

### `ps` - Display Processes

**Purpose**: Show running processes and their information.

```bash
ps                          # Show current shell processes
ps aux                      # Show all processes with details
ps -ef                      # Alternative format showing all
ps -u username              # Processes for specific user
ps aux | grep process_name  # Find specific process
ps -p PID                   # Show specific process by ID
ps --forest                 # Tree format (parent-child)
```

**Output Columns**:

- `USER` - Process owner
- `PID` - Process ID
- `%CPU` - CPU usage percentage
- `%MEM` - Memory usage percentage
- `COMMAND` - Command that started process

**Use Cases**:

- **Find process ID**: `ps aux | grep nginx` - Get Nginx PID
- **Monitor CPU/Memory**: `ps aux` - View resource usage
- **Tree view**: `ps --forest` - See process hierarchy

**Real-world Example**:

```bash
# Find and kill process
PID=$(ps aux | grep "[p]ython app.py" | awk '{print $2}')
kill $PID

# Check resource hogs
ps aux --sort=-%mem | head -5

# Monitor specific user's processes
ps -u www-data
```

-----

### `kill` - Terminate Processes

**Purpose**: Send signals to processes to terminate or control them.

```bash
kill PID                    # Send SIGTERM (graceful kill)
kill -9 PID                 # Send SIGKILL (force kill)
kill -TERM PID              # Explicit SIGTERM
kill -HUP PID               # Send SIGHUP (reload)
kill -STOP PID              # Pause process
kill -CONT PID              # Resume process
killall process_name        # Kill all processes by name
```

**Signal Numbers**:

- `1` (HUP) - Hangup
- `2` (INT) - Interrupt
- `9` (KILL) - Force kill
- `15` (TERM) - Terminate (default)
- `19` (STOP) - Stop
- `18` (CONT) - Continue

**Use Cases**:

- **Stop hung process**: `kill -9 $(pgrep process_name)`
- **Reload config**: `kill -HUP PID_nginx`
- **Graceful shutdown**: `kill PID` (allows cleanup)

**Real-world Example**:

```bash
# Kill stuck Node.js process
kill -9 $(lsof -ti:3000)

# Gracefully stop application
kill $(pgrep -f "java -jar app.jar")

# Kill all processes matching pattern
killall -9 node

# Reload Nginx gracefully
sudo kill -HUP $(cat /var/run/nginx.pid)
```

-----

### `top` - Monitor System Performance

**Purpose**: Real-time system monitoring and process management.

```bash
top                         # Interactive monitoring
top -b                      # Batch mode (non-interactive)
top -u username             # Monitor specific user
top -p PID                  # Monitor specific process
top -n 1                    # Single update then exit
top -d 2                    # Update every 2 seconds
```

**Interactive Commands in top**:

- `M` - Sort by memory usage
- `P` - Sort by CPU usage
- `T` - Sort by running time
- `k` - Kill process (enter PID)
- `q` - Quit

**Use Cases**:

- **Performance bottleneck**: Identify CPU/memory hogs
- **Health monitoring**: Regular system checks
- **Incident response**: Quick diagnosis during issues

**Real-world Example**:

```bash
# Monitor CPU-intensive processes
top -b -n 1 -o +%CPU | head -20

# Watch specific application
top -p $(pgrep -f "java -jar")

# Continuous monitoring output
top -b -d 1 -n 10 > monitoring.log
```

-----

### `htop` - Enhanced System Monitor

**Purpose**: Improved version of `top` with better interface.

```bash
htop                        # Start interactive monitoring
htop -u username            # Monitor specific user
htop -p PID                 # Monitor specific process
htop -s PERCENT_CPU         # Sort by CPU usage
```

**Advantages over top**:

- Color-coded output
- Better tree view
- Easier killing processes
- Scrollable lists

**Use Cases**:

- **Quick diagnosis**: Rapid performance assessment
- **Training**: Better for learning system monitoring
- **Multi-core view**: Clear CPU per-core display

-----

### `jobs` - Manage Background Jobs

**Purpose**: Display and manage background jobs in the shell.

```bash
jobs                        # List all jobs
jobs -l                     # List with process IDs
fg %1                       # Bring job 1 to foreground
bg %1                       # Resume job 1 in background
fg                          # Bring last job to foreground
command &                   # Start command in background
```

**Use Cases**:

- **Multitasking**: Run multiple operations concurrently
- **Long operations**: Run builds/tests in background
- **SSH sessions**: Keep operations running after disconnect

**Real-world Example**:

```bash
# Start long-running build in background
npm run build &

# List background jobs
jobs -l

# Bring to foreground to monitor
fg

# Run multiple tasks simultaneously
npm run lint &
npm run test &
npm run build &
wait
```

-----

### `nohup` - Run Commands Immune to Hangups

**Purpose**: Run processes that survive terminal disconnection.

```bash
nohup command > output.log &    # Run with output redirection
nohup command &                 # Run in background
nohup python script.py &        # Run Python script
```

**Use Cases**:

- **SSH sessions**: Keep processes running after logout
- **Long-running tasks**: Deployment, backups, builds
- **Server maintenance**: Continue operations during terminal issues

**Real-world Example**:

```bash
# Long-running backup
nohup tar -czf backup.tar.gz /var/www &

# Deployment that survives disconnect
nohup ./deploy.sh > deploy.log 2>&1 &

# Monitor with tail
tail -f nohup.out
```

-----

## Networking Commands

### `ping` - Test Network Connectivity

**Purpose**: Send ICMP packets to test host reachability.

```bash
ping -c 4 example.com       # Send 4 packets
ping -t 5 example.com       # Set timeout to 5 seconds
ping -i 0.5 example.com     # Set interval between packets
ping -s 56 example.com      # Set packet size
```

**Use Cases**:

- **Connectivity test**: `ping google.com` - Verify internet
- **Host availability**: `ping database.internal` - Check service host
- **Network diagnosis**: Identify latency or packet loss

**Real-world Example**:

```bash
# Check if server is up
ping -c 1 production.example.com && echo "Server UP" || echo "Server DOWN"

# Measure latency
ping -c 5 api.example.com | grep "time="
```

-----

### `ssh` - Secure Shell Remote Access

**Purpose**: Connect securely to remote systems.

```bash
ssh user@host               # Connect to host
ssh -p 2222 user@host       # Use custom port
ssh -i keyfile user@host    # Use specific key file
ssh -v user@host            # Verbose output (debug)
ssh -X user@host            # Enable X11 forwarding
ssh -N -f -L 3306:db:3306 user@host # Port forwarding
```

**Use Cases**:

- **Remote administration**: `ssh admin@server.com` - Access server
- **Development**: Work on remote machines
- **Tunneling**: `ssh -L 9200:elasticsearch:9200 user@bastion` - Create tunnel
- **Git operations**: SSH keys for GitHub/GitLab

**Real-world Example**:

```bash
# Connect with specific key
ssh -i ~/.ssh/production_key ubuntu@prod.example.com

# Tunnel database through bastion host
ssh -N -L 5432:db-internal:5432 user@bastion.company.com

# Execute remote command
ssh user@host "cd /app && git pull && npm run build"

# Copy SSH key to enable password-less auth
ssh-copy-id -i ~/.ssh/id_rsa.pub user@host
```

-----

### `scp` - Secure Copy Files

**Purpose**: Copy files between local and remote systems securely.

```bash
scp file.txt user@host:/path/ # Copy to remote
scp user@host:/path/file.txt . # Copy from remote
scp -r dir/ user@host:/path/  # Copy directory recursively
scp -P 2222 file.txt user@host:/path/ # Custom SSH port
scp user1@host1:/path/file.txt user2@host2:/path/ # Host to host
```

**Use Cases**:

- **Deployment**: `scp app.jar user@server:/opt/app/`
- **Backup**: `scp backup.tar.gz backup@storage:/backups/`
- **Configuration**: Transfer config files between servers

**Real-world Example**:

```bash
# Deploy application build
scp -r build/ ubuntu@production.example.com:/var/www/app/

# Backup logs
scp -r user@webserver:/var/log/app ~/local_backups/

# Copy database dump to restore
scp user@source:/backups/db.dump user@dest:/tmp/
```

-----

### `curl` - Transfer Data with URLs

**Purpose**: Retrieve data from or send data to URLs.

```bash
curl url                    # Fetch URL content
curl -o file.html url       # Save to file
curl -O url                 # Save with original name
curl -H "Header: value" url # Add custom header
curl -d "data" -X POST url  # POST request with data
curl -X PUT url             # PUT request
curl -i url                 # Include headers in output
curl -L url                 # Follow redirects
curl -u user:pass url       # Basic authentication
```

**Use Cases**:

- **API testing**: `curl -X POST -d '{}' https://api.example.com/users`
- **Download files**: `curl -O https://example.com/file.zip`
- **Health checks**: `curl -f http://localhost:8080/health || exit 1`
- **Monitoring**: Check endpoint availability

**Real-world Example**:

```bash
# Test API endpoint
curl -X POST -H "Content-Type: application/json" \
  -d '{"name":"John"}' \
  http://api.example.com/users

# Check server health
curl -s http://localhost:8080/health | jq .

# Download and verify
curl -O https://example.com/app.tar.gz
curl -O https://example.com/app.tar.gz.sha256
sha256sum -c app.tar.gz.sha256

# Monitor endpoint status
while true; do
    curl -s -o /dev/null -w "%{http_code}" http://localhost:8080
    sleep 5
done
```

-----

### `wget` - Download Files

**Purpose**: Download files from the internet non-interactively.

```bash
wget url                    # Simple download
wget -O filename url        # Save with custom name
wget -c url                 # Continue interrupted download
wget -r url                 # Recursive download (whole site)
wget --limit-rate=100k url  # Limit bandwidth
wget -q url                 # Quiet mode
```

**Use Cases**:

- **Bulk downloads**: `wget -r http://example.com/files/`
- **Resume download**: `wget -c partial_file_url`
- **Download with bandwidth limit**: `wget --limit-rate=500k large_file`

**Real-world Example**:

```bash
# Download specific file
wget https://example.com/package.tar.gz

# Download with resume capability
wget -c https://example.com/large-iso

# Recursive download of directory
wget -r https://example.com/docs/

# Background download with logging
wget -b -o download.log https://example.com/file.iso
```

-----

### `netstat` / `ss` - Network Statistics

**Purpose**: Display network connections and statistics.

```bash
netstat -tulpn              # All listening ports with programs
ss -tulpn                   # Modern alternative (faster)
netstat -an | grep ESTABLISHED # Active connections
netstat -i                  # Interface statistics
ss -s                       # Summary statistics
lsof -i :PORT               # Show process using port
```

**Use Cases**:

- **Port check**: `netstat -tulpn | grep 8080` - Is port listening?
- **Troubleshoot connections**: `ss -an | grep :3306` - MySQL connections
- **Security audit**: `netstat -tulpn` - Find unexpected services
- **Performance**: `netstat -i` - Check network interface stats

**Real-world Example**:

```bash
# Check if port is available
netstat -tulpn | grep :8080 || echo "Port 8080 available"

# List all listening services
ss -tulpn

# Monitor active connections
watch -n 1 'ss -an | grep ESTABLISHED | wc -l'

# Find process using specific port
lsof -i :3000
```

-----

### `ifconfig` / `ip` - Network Configuration

**Purpose**: Display or configure network interfaces.

```bash
ifconfig                    # Show all interfaces
ip addr show                # Modern alternative
ifconfig eth0               # Specific interface
ip addr show dev eth0       # Specific interface (modern)
ip route show               # Show routing table
ip link show                # Show link status
```

**Use Cases**:

- **Check IP address**: `ip addr show` - See all IPs
- **Debug networking**: `ifconfig -a` - Check interface status
- **Route verification**: `ip route show` - Verify routing config

**Real-world Example**:

```bash
# Get server IP address
IP=$(hostname -I | awk '{print $1}')
echo "Server IP: $IP"

# Check all network interfaces
ip link show

# View routing table
ip route
```

-----

## System Information

### `uname` - System Information

**Purpose**: Display system and kernel information.

```bash
uname -a                    # All information
uname -s                    # Kernel name (Linux)
uname -r                    # Kernel release
uname -m                    # Machine type (architecture)
uname -n                    # Network hostname
uname -p                    # Processor type
```

**Use Cases**:

- **Deployment validation**: Verify correct OS
- **Script adaptation**: Adjust for architecture
- **Documentation**: Record system specifications

**Real-world Example**:

```bash
# Build-specific logic
if [ "$(uname -m)" = "aarch64" ]; then
    ARCH="arm64"
else
    ARCH="x86_64"
fi

# Verify Linux system
[ "$(uname -s)" = "Linux" ] || { echo "Linux required"; exit 1; }
```

-----

### `df` - Disk Space Usage

**Purpose**: Display filesystem disk space usage.

```bash
df                          # Show all filesystems
df -h                       # Human-readable format
df -i                       # Show inode usage
df /path                    # Specific filesystem
df -H                       # SI units (1000 bytes)
```

**Use Cases**:

- **Capacity planning**: Check remaining space
- **Troubleshoot**: “Disk full” errors
- **Monitoring**: Alert on low space

**Real-world Example**:

```bash
# Check available space
df -h | grep "/$"

# Alert if root filesystem > 80% full
USAGE=$(df / | awk 'NR==2 {print $5}' | cut -d'%' -f1)
[ $USAGE -gt 80 ] && echo "Disk space critical!"

# Find filesystem with most usage
df -h | sort -k5 -rn
```

-----

### `du` - Directory Disk Usage

**Purpose**: Estimate file and directory space usage.

```bash
du -h dir/                  # Human-readable summary
du -sh dir/                 # Total size of directory
du -h --max-depth=1 dir/    # Size by subdirectory
du -s *.txt                 # Size of files
du -c dir1/ dir2/           # Combined total
```

**Use Cases**:

- **Find large directories**: `du -sh */ | sort -h` - Sort by size
- **Quota management**: Check usage per user
- **Cleanup**: Identify what uses most space

**Real-world Example**:

```bash
# Find top 10 largest directories
du -sh */ | sort -h | tail -10

# Check application size
du -sh /var/www/app

# Monitor log directory growth
du -sh /var/log/
```

-----

### `free` - Memory Usage

**Purpose**: Display memory usage statistics.

```bash
free                        # Memory in blocks
free -h                     # Human-readable
free -m                     # Megabytes
free -g                     # Gigabytes
free -s 5                   # Update every 5 seconds
```

**Use Cases**:

- **Performance tuning**: Identify memory pressure
- **Capacity planning**: Size applications appropriately
- **Troubleshooting**: Memory leak detection

**Real-world Example**:

```bash
# Check available memory
free -h

# Monitor memory every second
watch -n 1 'free -h'

# Calculate used memory percentage
TOTAL=$(free | awk 'NR==2{print $2}')
USED=$(free | awk 'NR==2{print $3}')
PERCENT=$((USED * 100 / TOTAL))
echo "Memory usage: ${PERCENT}%"
```

-----

### `uptime` - System Uptime

**Purpose**: Display how long system has been running.

```bash
uptime                      # Show uptime and load average
```

**Use Cases**:

- **Maintenance tracking**: Know last reboot
- **Performance correlation**: Relate issues to uptime
- **SLA monitoring**: Track system stability

**Real-world Example**:

```bash
# Daily monitoring report
echo "System uptime: $(uptime)"
echo "Date: $(date)" >> monitoring.log
```

-----

### `date` - Display/Set Date and Time

**Purpose**: Print or set the system date and time.

```bash
date                        # Current date and time
date "+%Y-%m-%d"           # Custom format (YYYY-MM-DD)
date "+%Y-%m-%d %H:%M:%S"  # Full timestamp
date "+%s"                  # Unix timestamp
date -d "2024-01-01"       # Parse specific date
date -d "+7 days"          # Date in future
```

**Use Cases**:

- **Log timestamps**: `echo "Event at $(date)" >> app.log`
- **Backup naming**: `tar -czf backup-$(date +%Y%m%d).tar.gz data/`
- **Scheduling**: Verify time for cron jobs

**Real-world Example**:

```bash
# Timestamped backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tar -czf backup_$TIMESTAMP.tar.gz /var/www/app

# Log with timestamp
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Application started" >> app.log

# Create dated directory
mkdir -p backups/$(date +%Y/%m/%d)
```

-----

## Text Processing and Searching

### `sort` - Sort Lines of Text

**Purpose**: Sort lines of text files.

```bash
sort file.txt               # Alphabetical sort
sort -r file.txt            # Reverse order
sort -n file.txt            # Numeric sort
sort -k2 file.txt           # Sort by column 2
sort -t: -k3 -n /etc/passwd # Sort by numeric column with delimiter
sort -u file.txt            # Sort and remove duplicates
sort -f file.txt            # Case-insensitive
```

**Use Cases**:

- **Organize data**: `sort data.csv > sorted.csv`
- **Remove duplicates**: `sort -u users.txt`
- **Parse logs**: `sort -k5 -rn access.log | head -10` - Top error codes

**Real-world Example**:

```bash
# Sort IP addresses by frequency
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# Parse password file by UID
sort -t: -k3 -n /etc/passwd | head -10

# Sort CSV by salary (column 4) descending
sort -t, -k4 -rn employees.csv
```

-----

### `uniq` - Filter Duplicate Lines

**Purpose**: Report or filter repeated lines.

```bash
uniq file.txt               # Remove adjacent duplicates
uniq -c file.txt            # Count occurrences
uniq -u file.txt            # Show only unique lines
uniq -d file.txt            # Show only duplicates
sort file.txt | uniq -c     # Count with sorting
```

**Use Cases**:

- **Remove duplicates**: `sort file.txt | uniq > unique.txt`
- **Count occurrences**: `sort file.txt | uniq -c | sort -rn` - Frequency analysis
- **Find duplicates**: `sort file.txt | uniq -d` - Which entries repeated

**Real-world Example**:

```bash
# Find duplicate entries in log
cat access.log | awk '{print $1}' | sort | uniq -d

# Count occurrences of each user login
cat /var/log/auth.log | grep "user" | awk '{print $NF}' | sort | uniq -c

# Find and remove duplicates in configuration
sort -u config.txt > config_unique.txt
```

-----

### `wc` - Word/Line/Character Count

**Purpose**: Count lines, words, characters in files.

```bash
wc file.txt                 # Lines, words, bytes
wc -l file.txt              # Lines only
wc -w file.txt              # Words only
wc -c file.txt              # Bytes only
wc -m file.txt              # Characters
wc -L file.txt              # Longest line length
wc -l *.txt                 # Multiple files
```

**Use Cases**:

- **Log size**: `wc -l access.log` - Number of log entries
- **Code metrics**: `wc -l src/*.py` - Lines of code
- **File validation**: Verify file size

**Real-world Example**:

```bash
# Count total lines of code
find src -name "*.js" | xargs wc -l | tail -1

# Count errors in log
grep ERROR app.log | wc -l

# Log file monitoring
wc -l access.log
# Check again later
wc -l access.log
```

-----

### `tr` - Translate Characters

**Purpose**: Translate or delete characters.

```bash
tr 'a-z' 'A-Z' < input.txt  # Lowercase to uppercase
tr -d ' ' < input.txt       # Delete spaces
tr ',' '\n' < input.csv     # Replace commas with newlines
tr -s ' ' ' ' < input.txt   # Squeeze multiple spaces
tr '[:lower:]' '[:upper:]'  # Alternative character classes
```

**Use Cases**:

- **Format conversion**: `tr ',' '\t' < data.csv > data.tsv`
- **Case conversion**: `tr '[:upper:]' '[:lower:]'` - Uppercase to lowercase
- **Cleanup**: `tr -d '[:space:]'` - Remove whitespace

**Real-world Example**:

```bash
# Convert CSV to space-separated
tr ',' ' ' < data.csv

# Remove all non-alphanumeric characters
tr -cd '[:alnum:]\n' < messy.txt

# Log format cleaning
cat raw.log | tr -s ' ' | tr ' ' ','
```

-----

## Package Management

### `apt/apt-get` - Debian Package Manager

**Purpose**: Install, update, and manage packages on Debian/Ubuntu.

```bash
apt update                  # Update package lists
apt upgrade                 # Upgrade all packages
apt install package-name    # Install package
apt remove package-name     # Remove package
apt autoremove              # Remove unused dependencies
apt search keyword          # Search for package
apt show package-name       # Package information
apt list --upgradable       # List upgradable packages
```

**Use Cases**:

- **System maintenance**: `sudo apt update && sudo apt upgrade`
- **Install software**: `sudo apt install nodejs python3`
- **Cleanup**: `sudo apt autoremove` - Remove unused packages

**Real-world Example**:

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install development tools
sudo apt install -y build-essential git curl wget

# Remove package and config
sudo apt remove --purge nginx
```

-----

### `yum/dnf` - RedHat Package Manager

**Purpose**: Package management for RedHat/CentOS/Fedora.

```bash
yum update                  # Update all packages
yum install package-name    # Install package
yum remove package-name     # Remove package
yum search keyword          # Search packages
yum info package-name       # Package info
dnf install package-name    # Modern alternative (Fedora)
```

**Use Cases**:

- **Enterprise environments**: CentOS, RHEL servers
- **Install dependencies**: `yum install gcc make`
- **Update system**: `yum update -y`

**Real-world Example**:

```bash
# Update system
sudo yum update -y

# Install web server
sudo yum install -y httpd mod_ssl

# Install development tools
sudo yum groupinstall -y "Development Tools"
```

-----

### `pip` - Python Package Manager

**Purpose**: Install and manage Python packages.

```bash
pip install package-name    # Install package
pip install --upgrade package-name # Upgrade package
pip uninstall package-name  # Remove package
pip list                    # List installed packages
pip search keyword          # Search packages
pip freeze > requirements.txt # Export dependencies
pip install -r requirements.txt # Install from file
```

**Use Cases**:

- **Python development**: Install libraries
- **Virtual environments**: `python -m venv venv && source venv/bin/activate`
- **Dependency management**: `pip freeze > requirements.txt`

**Real-world Example**:

```bash
# Set up Python project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install data science tools
pip install numpy pandas scikit-learn jupyter
```

-----

### `npm` - Node Package Manager

**Purpose**: Install and manage JavaScript packages.

```bash
npm install package-name    # Install package locally
npm install -g package-name # Install globally
npm uninstall package-name  # Remove package
npm list                    # List installed packages
npm search keyword          # Search packages
npm init                    # Initialize package.json
npm install                 # Install from package.json
npm update                  # Update packages
```

**Use Cases**:

- **Web development**: Install frameworks, tools
- **Project setup**: `npm init && npm install`
- **Build tools**: `npm install webpack typescript --save-dev`

**Real-world Example**:

```bash
# Initialize project
npm init -y
npm install express cors dotenv

# Install dev dependencies
npm install --save-dev webpack @babel/core

# Global CLI tools
npm install -g typescript ts-node
```

-----

## Compression and Archiving

### `tar` - Archive Files

**Purpose**: Archive and compress files.

```bash
tar -cf archive.tar files/  # Create uncompressed archive
tar -xf archive.tar         # Extract archive
tar -czf archive.tar.gz files/ # Create gzip compressed
tar -xzf archive.tar.gz     # Extract gzip
tar -cjf archive.tar.bz2 files/ # Create bzip2 compressed
tar -xjf archive.tar.bz2    # Extract bzip2
tar -tzf archive.tar.gz     # List contents
tar -xzf file.tar.gz -C /path/ # Extract to specific path
```

**Use Cases**:

- **Backup**: `tar -czf backup-$(date +%Y%m%d).tar.gz /var/www`
- **Distribution**: Create archive for sharing
- **Database backup**: `mysqldump db | tar -czf backup.sql.tar.gz -`

**Real-world Example**:

```bash
# Backup entire directory
tar -czf website-backup.tar.gz /var/www/html/

# Extract archive
tar -xzf website-backup.tar.gz

# Create incremental backup
tar -czf incremental-$(date +%Y%m%d).tar.gz --newer='2024-01-01' /var/www

# Backup with exclusions
tar -czf backup.tar.gz --exclude=node_modules --exclude=.git /app/
```

-----

### `gzip/gunzip` - Gzip Compression

**Purpose**: Compress or decompress files with gzip.

```bash
gzip file.txt               # Compress (creates file.txt.gz)
gunzip file.txt.gz          # Decompress
gzip -k file.txt            # Keep original file
gzip -r directory/          # Recursive compression
gzip -9 file.txt            # Maximum compression
zcat file.txt.gz            # View compressed file
```

**Use Cases**:

- **Log compression**: `gzip /var/log/app.log.*`
- **Reduce size**: Compress files for storage
- **Transmission**: Reduce bandwidth for transfer

**Real-world Example**:

```bash
# Compress old logs
find /var/log -name "*.log" -mtime +7 -exec gzip {} \;

# View compressed log without extracting
zcat /var/log/syslog.1.gz | head -20

# Compress and archive
tar --use-compress-program gzip -cf backup.tar.gz data/
```

-----

### `zip/unzip` - ZIP Compression

**Purpose**: Create and extract ZIP archives.

```bash
zip archive.zip file1 file2 # Create ZIP
unzip archive.zip           # Extract ZIP
zip -r archive.zip dir/     # ZIP directory recursively
unzip -l archive.zip        # List contents
unzip -d /path archive.zip  # Extract to directory
```

**Use Cases**:

- **Windows compatibility**: ZIP is widely supported
- **Distribution**: Package files for download
- **Selective compression**: Include/exclude files

**Real-world Example**:

```bash
# Create project archive
zip -r project.zip src/ docs/ -x "*/node_modules/*" "*/.*"

# Extract specific files
unzip archive.zip "src/*"

# Extract and preserve structure
unzip -d extracted/ archive.zip
```

-----

## Advanced System Administration

### `systemctl` - Manage System Services

**Purpose**: Control systemd services.

```bash
systemctl start service     # Start service
systemctl stop service      # Stop service
systemctl restart service   # Restart service
systemctl enable service    # Enable auto-start on boot
systemctl disable service   # Disable auto-start
systemctl status service    # Show service status
systemctl list-units --type=service # List all services
```

**Use Cases**:

- **Service management**: `sudo systemctl restart nginx`
- **Enable services**: `sudo systemctl enable postgresql`
- **Health monitoring**: `systemctl status` - Check all services

**Real-world Example**:

```bash
# Manage web application service
sudo systemctl restart app.service
sudo systemctl enable app.service
systemctl status app.service

# Check failed services
systemctl list-units --failed

# View service logs
journalctl -u nginx.service -n 50
```

-----

### `crontab` - Schedule Tasks

**Purpose**: Schedule periodic task execution.

```bash
crontab -e                  # Edit user crontab
crontab -l                  # List crontab entries
crontab -r                  # Remove crontab
sudo crontab -e             # Edit root crontab
```

**Cron Schedule Format**: `minute hour day month day-of-week command`

**Common Examples**:

```bash
# Every day at 2 AM
0 2 * * * /home/user/backup.sh

# Every 6 hours
0 */6 * * * /usr/local/bin/check_status.sh

# Every Monday at 9 AM
0 9 * * 1 /opt/maintenance.sh

# Every 5 minutes
*/5 * * * * /usr/bin/monitor.py

# First day of month at midnight
0 0 1 * * /root/monthly_report.sh
```

**Use Cases**:

- **Backups**: `0 2 * * * /scripts/backup.sh`
- **Monitoring**: `*/5 * * * * /scripts/health_check.sh`
- **Maintenance**: `0 3 * * 0 /scripts/cleanup.sh` - Weekly cleanup

**Real-world Example**:

```bash
# Backup database daily
0 2 * * * /usr/local/bin/backup_db.sh >> /var/log/backup.log 2>&1

# Rotate logs weekly
0 1 * * 0 /usr/sbin/logrotate /etc/logrotate.conf

# Check disk space daily
0 8 * * * /scripts/disk_check.sh | mail -s "Disk Report" admin@example.com
```

-----

### `find` - Search for Files

**Purpose**: Find files matching criteria.

```bash
find /path -name "*.txt"    # Find by name
find /path -type f         # Files only
find /path -type d         # Directories only
find /path -size +100M     # Larger than 100MB
find /path -mtime -7       # Modified in last 7 days
find /path -perm 644       # Specific permissions
find /path -user username  # Files owned by user
find /path -exec cmd {} \; # Execute command on matches
```

**Use Cases**:

- **Find large files**: `find / -size +1G -type f`
- **Recent changes**: `find /var/log -mtime -1 -type f` - Files modified today
- **Remove old files**: `find /tmp -type f -mtime +30 -delete` - Delete files 30+ days old
- **Batch operations**: `find src -name "*.js" -exec eslint {} \;`

**Real-world Example**:

```bash
# Find and delete old log files
find /var/log -name "*.log" -mtime +90 -delete

# Find large files in home directory
find ~ -type f -size +100M

# Find recently modified files
find . -type f -mmin -60

# Find files and apply command
find . -name "*.tmp" -exec rm {} \;

# Find Python files with trailing whitespace
find . -name "*.py" -exec grep -l '[[:space:]]$' {} \;
```

-----

### `lsof` - List Open Files

**Purpose**: Display open files and network connections.

```bash
lsof                        # List all open files
lsof -i                     # Show network connections
lsof -i :PORT               # Process using specific port
lsof -p PID                 # Files opened by process
lsof -u username            # Files opened by user
lsof /path/to/file          # Processes using file
```

**Use Cases**:

- **Port conflicts**: `lsof -i :8080` - What’s using this port?
- **Process debugging**: `lsof -p $$` - Files used by current shell
- **Device in use**: `lsof /dev/sda1` - What’s accessing disk
- **Deleted file recovery**: Find open deleted files

**Real-world Example**:

```bash
# Find what's using port 3000
lsof -i :3000

# List all network connections
lsof -i

# Check what process is holding file
lsof /var/log/app.log

# Monitor file access
lsof -r 5 /var/www/app/data.db
```

-----

### `watch` - Monitor Command Output

**Purpose**: Execute command repeatedly and display output.

```bash
watch command               # Update every 2 seconds (default)
watch -n 5 command          # Update every 5 seconds
watch -d command            # Highlight changes
watch 'command | pipeline'  # Complex commands with pipes
```

**Use Cases**:

- **Monitor logs**: `watch tail -20 app.log`
- **System stats**: `watch 'free -h'` - Monitor memory
- **Process tracking**: `watch 'ps aux | grep java'`
- **Build progress**: `watch make` - Keep checking build status

**Real-world Example**:

```bash
# Monitor system load
watch -n 1 'uptime && free -h && df -h /'

# Track deployment progress
watch 'docker ps --filter "name=myapp"'

# Monitor active connections
watch -d 'netstat -an | grep ESTABLISHED | wc -l'

# Watch log file in real-time
watch -n 1 'tail -5 /var/log/app.log'
```

-----

### `man` - Manual Pages

**Purpose**: Display manual pages for commands.

```bash
man command                 # Display command manual
man -k keyword              # Search manuals by keyword
man 5 config                # Section 5 (file formats)
man -a command              # Show all manual sections
```

**Manual Sections**:

- 1 - User commands
- 2 - System calls
- 3 - Library functions
- 5 - File formats
- 8 - System administration

**Use Cases**:

- **Learn syntax**: `man ls` - Full ls documentation
- **Troubleshoot**: `man 5 passwd` - Password file format
- **Reference**: `man grep` - grep options and examples

**Real-world Example**:

```bash
# Learn command thoroughly
man ssh

# Understand file format
man 5 /etc/passwd

# Search for commands related to files
man -k delete file
```

-----

## Summary

This comprehensive guide covers essential Linux commands used in:

- **Software development**: File management, git operations, deployment
- **System administration**: User management, service control, monitoring
- **DevOps**: Container orchestration, log analysis, performance monitoring
- **Troubleshooting**: Debugging, performance analysis, network diagnosis

**Best Practices**:

1. Always use `-i` flag with destructive commands (rm, mv) for confirmation
1. Test commands on non-production first
1. Use `sudo` carefully - verify commands before executing as root
1. Chain commands thoughtfully using pipes `|` for efficient processing
1. Document your automation with comments and logs
1. Use version control for scripts and configurations
1. Monitor execution of critical commands

**Quick Reference for Common Tasks**:

```bash
# System health check
echo "CPU:" && top -b -n 1 | head -5 && echo "Memory:" && free -h && echo "Disk:" && df -h

# Find large files
find / -type f -size +500M 2>/dev/null | head -10

# Search in files
grep -r "search_term" /path --include="*.ext"

# Bulk operations
for file in *.old; do mv "$file" "${file%.old}"; done

# Safe backup
cp -av important_file important_file.backup.$(date +%Y%m%d_%H%M%S)
```

Remember: Linux is powerful but dangerous - when in doubt, check the manual with `man command` or use `--help` flag.