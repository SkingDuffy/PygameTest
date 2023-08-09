# PygameTest



打包命令（模块名称首字母要大写）

python3 -m PyInstaller --onefile tank.py

python3 -m PyInstaller --onefile --noconsole --noconsole tank.py

python3 -m PyInstaller --onefile --noconsole --target-architecture arm64,x86_64 tank.py

打包后生成文件夹dist - 里面就是可执行文件
附带生成的文件build可删除
