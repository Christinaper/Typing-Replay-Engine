#!/usr/bin/env python3
"""
Typing Replay Engine - 快速启动脚本
Quick Start Launcher
"""

import sys
import os

def print_banner():
    """打印欢迎横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     ✨ Typing Replay Engine - 打字回放引擎 ✨            ║
║                                                           ║
║     版本: 1.0.0                                           ║
║     作者: Claude (Anthropic)                              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def show_menu():
    """显示主菜单"""
    print("\n请选择运行模式：\n")
    print("  1. 🖥️  启动 GUI 界面")
    print("  2. 📝  运行示例程序")
    print("  3. 🧪  运行测试")
    print("  4. 📖  查看文档")
    print("  5. ❌  退出\n")


def run_gui():
    """运行 GUI"""
    print("\n正在启动 GUI 界面...")
    try:
        import gui
        gui.main()
    except ImportError as e:
        print(f"错误: 无法导入 GUI 模块 - {e}")
        print("请确保所有依赖已安装。")
    except Exception as e:
        print(f"错误: {e}")


def run_examples():
    """运行示例"""
    print("\n示例列表：\n")
    examples = [
        "1. 基础打字",
        "2. 编辑与退格",
        "3. 选区与替换",
        "4. 代码编辑",
        "5. 样式切换",
        "6. JSON 脚本",
        "7. 脚本构建器",
        "8. 交互式模式",
        "9. Emoji 演示",
        "10. 帧导出",
        "0. 运行所有示例"
    ]
    
    for example in examples:
        print(f"  {example}")
    
    print()
    choice = input("请选择示例编号 (0-10): ").strip()
    
    try:
        import examples as ex
        
        if choice == '0':
            print("\n运行所有示例...")
            ex.run_all_examples()
        elif choice.isdigit() and 1 <= int(choice) <= 10:
            print(f"\n运行示例 {choice}...")
            os.system(f"python examples.py {choice}")
        else:
            print("无效的选择！")
    except Exception as e:
        print(f"错误: {e}")


def run_tests():
    """运行测试"""
    print("\n正在运行测试...")
    try:
        os.system("python test_engine.py")
    except Exception as e:
        print(f"错误: {e}")


def show_docs():
    """显示文档"""
    print("\n可用文档：\n")
    docs = [
        ("1", "README.md", "项目说明和快速入门"),
        ("2", "GUI_TUTORIAL.md", "GUI 使用教程"),
        ("3", "EXAMPLES_GALLERY.md", "实例参考库"),
        ("4", "ADVANCED_TUTORIAL.md", "高级教程"),
        ("5", "ARCHITECTURE.md", "架构设计"),
        ("6", "USE_CASES.md", "使用案例"),
    ]
    
    for num, filename, desc in docs:
        print(f"  {num}. {filename:25s} - {desc}")
    
    print()
    choice = input("请选择文档编号 (1-6, 0 返回): ").strip()
    
    doc_map = {str(i): filename for i, (_, filename, _) in enumerate(docs, 1)}
    
    if choice in doc_map:
        filename = doc_map[choice]
        if os.path.exists(filename):
            # 尝试用默认程序打开
            if sys.platform == 'darwin':  # macOS
                os.system(f"open {filename}")
            elif sys.platform == 'win32':  # Windows
                os.system(f"start {filename}")
            else:  # Linux
                os.system(f"xdg-open {filename} 2>/dev/null || cat {filename}")
        else:
            print(f"文件不存在: {filename}")


def main():
    """主函数"""
    print_banner()
    
    while True:
        show_menu()
        choice = input("请输入选项 (1-5): ").strip()
        
        if choice == '1':
            run_gui()
        elif choice == '2':
            run_examples()
        elif choice == '3':
            run_tests()
        elif choice == '4':
            show_docs()
        elif choice == '5':
            print("\n感谢使用！再见！👋\n")
            break
        else:
            print("\n❌ 无效的选项，请重新选择。\n")
        
        if choice in ['2', '3', '4']:
            input("\n按 Enter 继续...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已中断。再见！\n")
        sys.exit(0)
