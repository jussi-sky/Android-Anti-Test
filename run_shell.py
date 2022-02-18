import subprocess
import sys

def run(cmd, shell=False) -> (int, str):
    p = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = []
    while p.poll() is None:
        line = p.stdout.readline().strip()
        if line:
            line = _decode_data(line)
            result.append(line)
            print('{0}'.format(line))
        # 清空缓存
        sys.stdout.flush()
        sys.stderr.flush()
    return p.returncode, '\r\n'.join(result)


def _decode_data(byte_data: bytes):
    try:
        return byte_data.decode('UTF-8')
    except UnicodeDecodeError:
        return byte_data.decode('GB18030')

if __name__ == '__main__':
    return_code, data = run('ping www.baidu.com')
    print('return code:', return_code, 'data:', data)
