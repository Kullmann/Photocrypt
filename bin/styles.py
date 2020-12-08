def green_button_style(width = None, height = None):
    """
    Green button style
    """
    width_style = f"width: {width};" if width else ""
    height_style = f"height: {width};" if height else ""
    style = f"""
    QPushButton {{
        background-color: #28a745;
        color: #ffffff;
        border-radius: 10px;
        {width_style}
        {height_style}
    }}
    QPushButton:hover {{ background-color: #218838 }}
    QPushButton:pressed {{
        background-color: #218838;
        border: 3px solid #1e7e34;
    }}
    """
    return style

def blue_button_style(width = None, height = None):
    """
    Blue button style
    """
    width_style = f"width: {width}px;" if width else ""
    height_style = f"height: {height}px;" if height else ""
    style = f"""
    QPushButton {{
        background-color: #007bff;
        color: #ffffff;
        border-radius: 10px;
        {width_style}
        {height_style}
    }}
    QPushButton:hover {{ background-color: #0069d9 }}
    QPushButton:pressed {{
        background-color: #0069d9;
        border: 3px solid #0062cc;
    }}
    """
    return style

def red_button_style(width = None, height = None):
    """
    Blue button style
    """
    width_style = f"width: {width}px;" if width else ""
    height_style = f"height: {height}px;" if height else ""
    style = f"""
    QPushButton {{
        background-color: #d9534f;
        color: #ffffff;
        border-radius: 10px;
        {width_style}
        {height_style}
    }}
    QPushButton:hover {{ background-color: #c9302c }}
    QPushButton:pressed {{
        background-color: #ac2925;
        border: 3px solid #761c19;
    }}
    """
    return style

def disabled_button_style(width = None, height = None):
    """
    Blue button style
    """
    width_style = f"width: {width}px;" if width else ""
    height_style = f"height: {height}px;" if height else ""
    style = f"""
    QPushButton {{
        background-color: gray;
        color: #ffffff;
        border-radius: 10px;
        {width_style}
        {height_style}
    }}
    """
    return style
