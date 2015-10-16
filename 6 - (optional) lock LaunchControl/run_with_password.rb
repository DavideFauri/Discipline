#!/usr/bin/env ruby
# run an app at lower privilege

require 'etc'
require 'find'

# Note: anyone with sudo access will be able to run as this user. But they could do that anyway.
# run 'id' at the terminal to find out what your username is.
RUN_USER = 'Da'

def get_root_info
  root_entry = Etc.getpwnam('root')
  return root_entry.uid, root_entry.gid
end

ROOT_UID, ROOT_GID = get_root_info

def ensure_root
  Process.uid = ROOT_UID
  Process.gid = ROOT_GID
end

def print_user_info
  [
   [:uid, Process.uid],
   [:gid, Process.gid],
   [:euid, Process.euid],
   [:egid, Process.egid],
  ].each do |arr|
    $stderr.puts arr.inspect
  end
end

def set_effective(euid, egid)
  $stderr.puts "setting effective to #{[euid, egid].inspect}"  if $DEBUG
  # must set group first
  Process.egid = egid
  Process.euid = euid
end

def do_privileged(&block)
  orig_euid = Process.euid
  orig_egid = Process.egid
  begin
    $stderr.puts "raising privileges"  if $DEBUG
    set_effective(ROOT_UID, ROOT_GID)
    yield orig_euid, orig_egid
  ensure
    $stderr.puts "lowering privileges"  if $DEBUG
    set_effective(orig_euid, orig_egid)
  end
end

# must be called after ROOT_UID, ROOT_GID are set
def chmod_files_in_dir(mode, dir)
  mode_str = nil
  case mode
  when Integer
    mode_str = '%o' % mode
  when String
    mode_str = mode
  else
    raise TypeError
  end
  chmod_proc = proc do
    Find.find(dir) {|entry|
      if File.directory?(entry) and entry != dir
        Find.prune  # don't recurse into subdirs
      elsif File.file?(entry)
        $stderr.puts "chmod #{mode_str} #{entry}"  if $DEBUG
        system 'chmod', mode_str, entry
      end
    }
  end
  # assume that if dir is owned by root, the executables are also.
  if File.stat(dir).uid == ROOT_UID
    do_privileged(&chmod_proc)
  else
    chmod_proc.call
  end
end

def main(argv)
  # Important: this is to abort if we're not running as root.
  ensure_root

  app_path = argv.shift or raise "Need path to .app file, e.g. /Applications/Mail.app"
  app_macos_dir = File.join(app_path, 'Contents/MacOS')
  File.directory?(app_path) or raise "#{app_path} is not an app bundle"
  File.directory?(app_macos_dir) or raise "#{app_path} bundle doesn't have expected MacOS structure"

  pw_entry = Etc.getpwnam(RUN_USER)
  run_uid = pw_entry.uid
  run_gid = pw_entry.gid


  if $DEBUG
    $stderr.puts [:run_uid, run_uid].inspect
    $stderr.puts [:run_gid, run_gid].inspect
    print_user_info
  end

  # Effectively become RUN_USER
  set_effective(run_uid, run_gid)

  if $DEBUG
    print_user_info
  end

  begin
    chmod_files_in_dir('+x', app_macos_dir)
    # 'open' is asynchronous, so the ensure will run immediately after, and before the app exits.
    $stderr.puts "Running app: #{app_path}"  if $DEBUG
    system 'open', app_path
  ensure
    chmod_files_in_dir('-x', app_macos_dir)
  end
end

if __FILE__ == $0
  $DEBUG = false
  main(ARGV)
end