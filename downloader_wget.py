import subprocess


if __name__ == '__main__':
    # 指定包含URLs的文本文件路径
    urls_file = 'C:\\Users\\David\\Desktop\\test2\\urls.txt'

    # 用户名和密码
    username = 'LIUcq'
    password = '456213caiqinA!'

    # 读取URLs文件
    with open(urls_file, 'r') as file:
        urls = file.readlines()

    # 遍历每个URL
    for url in urls:
        url = url.strip()  # 移除字符串头尾的空白符
        # 从URL中提取文件名
        filename = 'C:\\Users\\David\\Desktop\\test2\\out\\' + url.split('/')[-1]

        # 构建wget命令，包括用户名和密码，以及指定输出文件名
        command = ['wget', '--user', username, '--password', password,
                   '--load-cookies','C:\\Users\\David\\\Desktop\\test2\\.urs_cookies',
                   '--save-cookies', 'C:\\Users\\David\\\Desktop\\test2\\out\\.urs_cookies',
                   '--auth-no-challenge=on',
                   '-O', filename, url]
        print(' '.join(command))
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        # 打印标准输出和标准错误
        if result.stdout:
            print("Standard Output:", result.stdout)
        if result.stderr:
            print("Error:", result.stderr)

    print("All downloads completed.")