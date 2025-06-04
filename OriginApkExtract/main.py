import os
import subprocess

# 本地保存的根目录
DEST_ROOT = "./pulled_system_apps"

def run_adb_command(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if result.returncode != 0:
        print(f"ADB 命令错误：{result.stderr.strip()}")
        return []
    return result.stdout.strip().splitlines()

def list_system_apps():
    print("正在获取系统应用列表...")
    lines = run_adb_command("adb shell pm list packages -f")
    apk_paths = []
    for line in lines:
        if line.startswith("package:"):
            try:
                raw = line[len("package:"):]
                apk_path, _ = raw.rsplit('=', 1)  # 从右侧切一次，防止路径中包含等号
                apk_paths.append(apk_path)
            except Exception as e:
                print(f"解析错误：{line}, 错误：{e}")
    return apk_paths

def pull_apks(apk_paths):
    for apk_path in apk_paths:
        # 保持原有目录结构
        relative_path = apk_path.lstrip("/")
        dest_path = os.path.join(DEST_ROOT, relative_path)

        # 创建本地目录
        dest_dir = os.path.dirname(dest_path)
        os.makedirs(dest_dir, exist_ok=True)

        print(f"正在拉取：{apk_path} -> {dest_path}")
        result = subprocess.run(f'adb pull "{apk_path}" "{dest_path}"', shell=True)
        if result.returncode != 0:
            print(f"拉取失败：{apk_path}")

if __name__ == "__main__":
    apk_paths = list_system_apps()
    print(f"共发现 {len(apk_paths)} 个系统应用")
    pull_apks(apk_paths)
