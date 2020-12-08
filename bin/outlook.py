"""
open email client operation
"""
import pathlib
import platform
import webbrowser
from os.path import dirname, join, realpath

SUPPORTED_OS = ['Windows']
PR_ATTACH_CONTENT_ID = "http://schemas.microsoft.com/mapi/proptag/0x3712001F"
WORKING_DIRECTORY = dirname(realpath(__file__))

if platform.system() in SUPPORTED_OS:
    import win32com.client as client

def open_outlook_client(img_path: str, email: str="", subject: str="") -> None:
    """
    opens up outlook client.
    If os not supported, it opens up mail to instead.

        Parameters:
            img_path (str): image to send
            email (str): email to send image
            subject (str): subject to send image
    """

    if platform.system() not in SUPPORTED_OS:
        # for OS that doesn't support win32 api.
        webbrowser.open(f"mailto:?to={email}&subject={subject}", new=1)
        return

    img_abs = str(pathlib.Path(img_path).absolute())

    outlook = client.Dispatch('Outlook.Application')
    message = outlook.CreateItem(0)
    message.Display()

    message.To, message.Subject = email, subject

    image = message.Attachments.Add(img_abs)

    with open(join(WORKING_DIRECTORY, "template.html")) as file:
        html = file.read()

    image.PropertyAccessor.SetProperty(PR_ATTACH_CONTENT_ID, "encrypted_img")
    message.HTMLBODY = html
