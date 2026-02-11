"""
Typing Replay Engine - GUI 界面
基于 Tkinter 的简洁美观图形界面
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
from pathlib import Path
import threading
import time

# 导入核心模块
from buffer import TextBuffer, TextStyle
from actions import (
    type_text, pause, backspace, move_cursor, select,
    delete_selection, set_style, TypeTextAction, InsertTextAction,
    BackspaceAction, DeleteAction, ReplaceTextAction
)
from scheduler import PlaybackScheduler, InteractiveScheduler
from script_parser import ScriptParser, ScriptBuilder, load_demo_script
from console import SimpleDisplay


class TypingReplayGUI:
    """打字回放引擎 GUI 主窗口"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Replay Engine - 打字回放引擎")
        self.root.geometry("1200x800")
        
        # 设置样式
        self.setup_styles()
        
        # 初始化变量
        self.scheduler = None
        self.is_playing = False
        self.current_script = None
        
        # 创建界面
        self.create_widgets()
        
        # 加载默认示例
        self.load_demo_script("hello_world")
    
    def setup_styles(self):
        """设置主题样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配色方案
        self.colors = {
            'bg': '#f5f5f5',
            'fg': '#2c3e50',
            'primary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'secondary': '#95a5a6',
            'editor_bg': '#ffffff',
            'editor_fg': '#2c3e50',
        }
        
        # 配置样式
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('TButton', padding=8)
        style.configure('Primary.TButton', foreground=self.colors['primary'])
        style.configure('Success.TButton', foreground=self.colors['success'])
        style.configure('Danger.TButton', foreground=self.colors['danger'])
        
        self.root.configure(bg=self.colors['bg'])
    
    def create_widgets(self):
        """创建所有界面组件"""
        # 主容器
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # 创建各个区域
        self.create_toolbar(main_container)
        self.create_editor_area(main_container)
        self.create_control_panel(main_container)
        self.create_preview_area(main_container)
        self.create_status_bar(main_container)
    
    def create_toolbar(self, parent):
        """创建工具栏"""
        toolbar = ttk.Frame(parent)
        toolbar.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 标题
        title = ttk.Label(
            toolbar, 
            text="✨ Typing Replay Engine",
            font=('Helvetica', 16, 'bold'),
            foreground=self.colors['primary']
        )
        title.pack(side=tk.LEFT, padx=10)
        
        # 工具按钮
        btn_frame = ttk.Frame(toolbar)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            btn_frame, 
            text="📂 打开脚本",
            command=self.load_script_file,
            style='Primary.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="💾 保存脚本",
            command=self.save_script_file,
            style='Primary.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="🎬 演示脚本",
            command=self.show_demo_menu,
            style='Primary.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="📖 帮助",
            command=self.show_help,
            style='Primary.TButton'
        ).pack(side=tk.LEFT, padx=5)
    
    def create_editor_area(self, parent):
        """创建脚本编辑区"""
        editor_frame = ttk.LabelFrame(parent, text="脚本编辑器", padding="10")
        editor_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # 编辑器
        self.script_editor = scrolledtext.ScrolledText(
            editor_frame,
            width=50,
            height=30,
            font=('Consolas', 10),
            bg=self.colors['editor_bg'],
            fg=self.colors['editor_fg'],
            insertbackground=self.colors['primary'],
            wrap=tk.WORD
        )
        self.script_editor.pack(fill=tk.BOTH, expand=True)
        
        # 编辑器工具栏
        editor_tools = ttk.Frame(editor_frame)
        editor_tools.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(
            editor_tools,
            text="✓ 验证脚本",
            command=self.validate_script,
            style='Success.TButton'
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            editor_tools,
            text="⟲ 重置",
            command=self.reset_script,
            style='Danger.TButton'
        ).pack(side=tk.LEFT, padx=2)
    
    def create_control_panel(self, parent):
        """创建控制面板"""
        control_frame = ttk.LabelFrame(parent, text="播放控制", padding="10")
        control_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 预览区域
        preview_label = ttk.Label(control_frame, text="实时预览:", font=('Helvetica', 11, 'bold'))
        preview_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.preview_text = scrolledtext.ScrolledText(
            control_frame,
            width=60,
            height=20,
            font=('Consolas', 11),
            bg='#fefefe',
            fg=self.colors['editor_fg'],
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 控制按钮区
        controls = ttk.Frame(control_frame)
        controls.pack(fill=tk.X, pady=5)
        
        # 播放速度
        speed_frame = ttk.Frame(controls)
        speed_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(speed_frame, text="播放速度:").pack(side=tk.LEFT, padx=5)
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(
            speed_frame,
            from_=0.1,
            to=3.0,
            variable=self.speed_var,
            orient=tk.HORIZONTAL,
            length=200
        )
        speed_scale.pack(side=tk.LEFT, padx=5)
        
        self.speed_label = ttk.Label(speed_frame, text="1.0x")
        self.speed_label.pack(side=tk.LEFT, padx=5)
        
        self.speed_var.trace('w', self.update_speed_label)
        
        # 播放按钮
        btn_frame = ttk.Frame(controls)
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.play_btn = ttk.Button(
            btn_frame,
            text="▶ 播放",
            command=self.play_script,
            style='Success.TButton'
        )
        self.play_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.pause_btn = ttk.Button(
            btn_frame,
            text="⏸ 暂停",
            command=self.pause_script,
            state=tk.DISABLED
        )
        self.pause_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.stop_btn = ttk.Button(
            btn_frame,
            text="⏹ 停止",
            command=self.stop_script,
            state=tk.DISABLED,
            style='Danger.TButton'
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 步进控制
        step_frame = ttk.Frame(controls)
        step_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(step_frame, text="步进模式:").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            step_frame,
            text="◀ 上一步",
            command=self.step_back,
            width=12
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            step_frame,
            text="▶ 下一步",
            command=self.step_forward,
            width=12
        ).pack(side=tk.LEFT, padx=2)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(
            controls,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress.pack(fill=tk.X, pady=10)
        
        self.progress_label = ttk.Label(controls, text="就绪")
        self.progress_label.pack()
    
    def create_preview_area(self, parent):
        """创建预览信息区"""
        # 这部分已经整合到 control_panel 中
        pass
    
    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = ttk.Label(
            status_frame,
            text="就绪",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.stats_label = ttk.Label(
            status_frame,
            text="行: 0 | 字符: 0",
            relief=tk.SUNKEN,
            anchor=tk.E
        )
        self.stats_label.pack(side=tk.RIGHT)
    
    # ==================== 事件处理 ====================
    
    def update_speed_label(self, *args):
        """更新速度标签"""
        speed = self.speed_var.get()
        self.speed_label.config(text=f"{speed:.1f}x")
    
    def validate_script(self):
        """验证脚本格式"""
        try:
            script_text = self.script_editor.get("1.0", tk.END)
            script = json.loads(script_text)
            actions = ScriptParser.parse(script)
            
            messagebox.showinfo(
                "验证成功",
                f"脚本有效！\n共 {len(actions)} 个动作"
            )
            self.update_status("脚本验证通过 ✓", "success")
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON 错误", f"脚本格式错误:\n{str(e)}")
            self.update_status("脚本验证失败 ✗", "error")
        except Exception as e:
            messagebox.showerror("错误", f"脚本错误:\n{str(e)}")
            self.update_status("脚本验证失败 ✗", "error")
    
    def reset_script(self):
        """重置脚本编辑器"""
        if messagebox.askyesno("确认", "确定要重置脚本吗？"):
            self.load_demo_script("hello_world")
            self.clear_preview()
            self.update_status("脚本已重置")
    
    def load_script_file(self):
        """加载脚本文件"""
        filename = filedialog.askopenfilename(
            title="选择脚本文件",
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    script_text = f.read()
                
                self.script_editor.delete("1.0", tk.END)
                self.script_editor.insert("1.0", script_text)
                
                self.update_status(f"已加载: {Path(filename).name}")
            except Exception as e:
                messagebox.showerror("错误", f"加载文件失败:\n{str(e)}")
    
    def save_script_file(self):
        """保存脚本文件"""
        filename = filedialog.asksaveasfilename(
            title="保存脚本",
            defaultextension=".json",
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if filename:
            try:
                script_text = self.script_editor.get("1.0", tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(script_text)
                
                self.update_status(f"已保存: {Path(filename).name}")
                messagebox.showinfo("成功", "脚本已保存！")
            except Exception as e:
                messagebox.showerror("错误", f"保存文件失败:\n{str(e)}")
    
    def show_demo_menu(self):
        """显示演示脚本菜单"""
        demo_window = tk.Toplevel(self.root)
        demo_window.title("选择演示脚本")
        demo_window.geometry("400x300")
        demo_window.transient(self.root)
        
        ttk.Label(
            demo_window,
            text="选择一个演示脚本:",
            font=('Helvetica', 11, 'bold')
        ).pack(pady=10)
        
        demos = [
            ("hello_world", "Hello World - 基础示例"),
            ("code_editing", "代码编辑 - 编程示例"),
            ("emoji_demo", "Emoji 演示")
        ]
        
        for demo_id, demo_name in demos:
            btn = ttk.Button(
                demo_window,
                text=demo_name,
                command=lambda d=demo_id: [
                    self.load_demo_script(d),
                    demo_window.destroy()
                ]
            )
            btn.pack(fill=tk.X, padx=20, pady=5)
    
    def load_demo_script(self, demo_name):
        """加载演示脚本"""
        try:
            from script_parser import DEMO_SCRIPTS
            
            if demo_name in DEMO_SCRIPTS:
                script = DEMO_SCRIPTS[demo_name]
                script_text = json.dumps(script, indent=2, ensure_ascii=False)
                
                self.script_editor.delete("1.0", tk.END)
                self.script_editor.insert("1.0", script_text)
                
                self.update_status(f"已加载演示: {demo_name}")
        except Exception as e:
            messagebox.showerror("错误", f"加载演示失败:\n{str(e)}")
    
    def show_help(self):
        """显示帮助窗口"""
        help_window = tk.Toplevel(self.root)
        help_window.title("使用帮助")
        help_window.geometry("600x500")
        help_window.transient(self.root)
        
        help_text = scrolledtext.ScrolledText(
            help_window,
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        help_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        help_content = """
Typing Replay Engine - 使用帮助
================================

1. 脚本格式
-----------
使用 JSON 格式定义动作序列:

{
  "actions": [
    {"type": "type", "text": "Hello", "wpm": 60},
    {"type": "pause", "duration": 0.5},
    {"type": "backspace", "count": 5}
  ]
}

2. 支持的动作类型
----------------
- type: 打字动作 (参数: text, wpm)
- insert: 即时插入 (参数: text)
- pause: 停顿 (参数: duration)
- backspace: 退格 (参数: count)
- delete: Delete 键 (参数: count)
- move_cursor: 光标移动 (参数: position 或 offset)
- select: 创建选区 (参数: start, end)
- delete_selection: 删除选区

3. 播放控制
-----------
- 播放速度: 调整滑块控制播放速度 (0.1x - 3.0x)
- 步进模式: 逐步执行每个动作，便于调试
- 实时预览: 查看打字效果

4. 快捷键
---------
- Ctrl+O: 打开脚本
- Ctrl+S: 保存脚本
- Space: 播放/暂停

5. 提示
-------
- 使用"验证脚本"确保格式正确
- 尝试不同的演示脚本学习用法
- 调整播放速度查看细节

更多信息请访问项目文档。
        """
        
        help_text.insert("1.0", help_content)
        help_text.config(state=tk.DISABLED)
    
    def play_script(self):
        """播放脚本 - 真正的逐字显示"""
        if self.is_playing:
            return
        
        try:
            # 解析脚本
            script_text = self.script_editor.get("1.0", tk.END)
            script = json.loads(script_text)
            actions = ScriptParser.parse(script)
            
            # 创建调度器
            self.scheduler = PlaybackScheduler()
            self.scheduler.add_actions(actions)
            
            # 更新 UI 状态
            self.is_playing = True
            self.play_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.NORMAL)
            
            self.clear_preview()
            self.update_status("播放中...")
            
            # 启动光标闪烁
            self.start_cursor_blink()
            
            # 在新线程中播放
            speed = self.speed_var.get()
            play_thread = threading.Thread(
                target=self._play_char_by_char,
                args=(actions, speed),
                daemon=True
            )
            play_thread.start()
            
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON 错误", f"脚本格式错误:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("错误", f"播放失败:\n{str(e)}")
            self.reset_playback_state()
    
    def _play_char_by_char(self, actions, speed):
        """逐字符播放动作"""
        try:
            buffer = TextBuffer()
            total_actions = len(actions)
            
            for action_idx, action in enumerate(actions):
                if not self.is_playing:
                    break
                
                # 处理不同类型的动作
                if isinstance(action, TypeTextAction):
                    # 逐字符打字
                    for char_idx in range(len(action.text)):
                        if not self.is_playing:
                            break
                        
                        buffer.insert_text(action.text[char_idx])
                        self.root.after(0, self.update_preview_from_buffer, buffer)
                        
                        # 计算延迟
                        delay = action.get_char_delay(char_idx) / speed
                        time.sleep(delay)
                
                elif isinstance(action, BackspaceAction):
                    # 逐字符删除
                    for step in range(action.count):
                        if not self.is_playing:
                            break
                        
                        buffer.delete_char(forward=False)
                        self.root.after(0, self.update_preview_from_buffer, buffer)
                        
                        delay = action.char_delay / speed
                        time.sleep(delay)
                
                elif isinstance(action, DeleteAction):
                    # 逐字符删除
                    for step in range(action.count):
                        if not self.is_playing:
                            break
                        
                        buffer.delete_char(forward=True)
                        self.root.after(0, self.update_preview_from_buffer, buffer)
                        
                        delay = action.char_delay / speed
                        time.sleep(delay)
                
                else:
                    # 其他动作一次性执行
                    action.execute(buffer)
                    self.root.after(0, self.update_preview_from_buffer, buffer)
                    
                    delay = action.get_duration() / speed
                    if delay > 0:
                        time.sleep(delay)
                
                # 更新进度
                progress = ((action_idx + 1) / total_actions) * 100
                self.root.after(0, self.progress_var.set, progress)
            
            # 播放完成
            self.root.after(0, self._playback_finished)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("播放错误", str(e)))
            self.root.after(0, self.reset_playback_state)
    
    def update_preview_from_buffer(self, buffer):
        """从 buffer 更新预览"""
        state = buffer.get_state(0)
        self.update_preview(state)
    
    def start_cursor_blink(self):
        """启动光标闪烁"""
        self.cursor_visible = True
        self.blink_cursor()
    
    def stop_cursor_blink(self):
        """停止光标闪烁"""
        self.cursor_visible = False
        if hasattr(self, 'blink_job'):
            self.root.after_cancel(self.blink_job)
    
    def blink_cursor(self):
        """光标闪烁动画"""
        if not self.is_playing:
            return
        
        # 切换光标可见性
        self.cursor_visible = not self.cursor_visible
        
        # 重新渲染预览（会根据 cursor_visible 决定是否显示光标）
        if hasattr(self, 'current_buffer_state'):
            self.update_preview(self.current_buffer_state)
        
        # 每 500ms 切换一次
        self.blink_job = self.root.after(500, self.blink_cursor)
    
    def _playback_finished(self):
        """播放完成回调"""
        self.stop_cursor_blink()
        self.update_status("播放完成 ✓", "success")
        self.progress_var.set(100)
        self.reset_playback_state()
        messagebox.showinfo("完成", "脚本播放完成！")
    
    def pause_script(self):
        """暂停播放（简化版）"""
        self.update_status("暂停功能待实现")
    
    def stop_script(self):
        """停止播放"""
        self.is_playing = False
        self.scheduler = None
        self.stop_cursor_blink()
        self.reset_playback_state()
        self.clear_preview()
        self.update_status("已停止")
    
    def step_forward(self):
        """单步前进"""
        try:
            script_text = self.script_editor.get("1.0", tk.END)
            script = json.loads(script_text)
            actions = ScriptParser.parse(script)
            
            if not hasattr(self, 'interactive_scheduler') or self.interactive_scheduler is None:
                self.interactive_scheduler = InteractiveScheduler()
                self.interactive_scheduler.add_actions(actions)
            
            if not self.interactive_scheduler.is_finished():
                event = self.interactive_scheduler.step()
                if event:
                    self.update_preview(event.state_after)
                    progress = self.interactive_scheduler.get_progress() * 100
                    self.progress_var.set(progress)
                    self.update_status(f"步进: {progress:.1f}%")
            else:
                self.update_status("已到达末尾")
                
        except Exception as e:
            messagebox.showerror("错误", f"步进失败:\n{str(e)}")
    
    def step_back(self):
        """单步后退"""
        if hasattr(self, 'interactive_scheduler') and self.interactive_scheduler:
            if self.interactive_scheduler.step_back():
                state = self.interactive_scheduler.get_current_state()
                self.update_preview(state)
                progress = self.interactive_scheduler.get_progress() * 100
                self.progress_var.set(progress)
                self.update_status(f"步进: {progress:.1f}%")
            else:
                self.update_status("已到达开头")
    
    def reset_playback_state(self):
        """重置播放状态"""
        self.is_playing = False
        self.play_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
    
    def update_preview(self, state):
        """更新预览文本"""
        # 保存当前状态
        self.current_buffer_state = state
        
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete("1.0", tk.END)
        
        # 显示文本
        text = state.text
        cursor = state.cursor_pos
        
        # 插入文本和光标标记
        if text:
            before_cursor = text[:cursor]
            after_cursor = text[cursor:]
            
            self.preview_text.insert("1.0", before_cursor)
            
            # 根据闪烁状态决定是否显示光标
            if hasattr(self, 'cursor_visible') and self.cursor_visible:
                self.preview_text.insert(tk.END, "|", "cursor")
            else:
                self.preview_text.insert(tk.END, " ", "cursor_space")
            
            self.preview_text.insert(tk.END, after_cursor)
        else:
            # 空文本时显示光标
            if hasattr(self, 'cursor_visible') and self.cursor_visible:
                self.preview_text.insert("1.0", "|", "cursor")
        
        # 配置光标样式
        self.preview_text.tag_config("cursor", foreground=self.colors['primary'], font=('Consolas', 11, 'bold'))
        self.preview_text.tag_config("cursor_space", foreground=self.colors['editor_bg'])
        
        self.preview_text.config(state=tk.DISABLED)
        
        # 更新统计
        lines = text.count('\n') + 1 if text else 0
        chars = len(text)
        self.stats_label.config(text=f"行: {lines} | 字符: {chars} | 光标: {cursor}")
    
    def clear_preview(self):
        """清空预览"""
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.config(state=tk.DISABLED)
        self.stats_label.config(text="行: 0 | 字符: 0")
    
    def update_status(self, message, status_type="normal"):
        """更新状态栏"""
        colors = {
            "normal": self.colors['fg'],
            "success": self.colors['success'],
            "error": self.colors['danger'],
            "warning": self.colors['warning']
        }
        
        self.status_label.config(
            text=message,
            foreground=colors.get(status_type, colors["normal"])
        )


def main():
    """主函数"""
    root = tk.Tk()
    app = TypingReplayGUI(root)
    
    # 设置窗口图标（可选）
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    # 居中窗口
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == '__main__':
    main()
