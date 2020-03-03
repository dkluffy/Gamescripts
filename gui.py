import win32gui

CLIP_COORDS = False

# def dec_clipper(func):
#     def clipper(*args):
#         result = func(*args)


def winEnumHandler(hwnd, ctx):
    """
    https://docs.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-enumwindows
    """
    if win32gui.IsWindowVisible( hwnd ):
        txt = win32gui.GetWindowText(hwnd)
        ctx[hwnd]=txt

def enumWindows():
    """
    return: dict{句柄:窗口名字} 包含所有可见窗口的字典 
    """
    wins = {}
    win32gui.EnumWindows(winEnumHandler, wins)
    return wins


def getWindowsRectByName(name):
    """
    return: [] 包含name的窗口的坐标 tagRECT

    typedef struct tagRECT {
          LONG left;
          LONG top;
          LONG right;
          LONG bottom;
        } RECT, *PRECT, *NPRECT, *LPRECT;
    BUG:在4K显示器下，最大只能显示2K
    """
    wins = enumWindows()
    result = []
    for k,v in wins.items():
        if name in v:
            result.append(win32gui.GetWindowRect(k))
    return result

if __name__ == "__main__":
    print(getWindowsRectByName("Chrome"))