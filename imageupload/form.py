from django import forms

class UploadImageForm(forms.Form):
    """图像上传表单"""
    #text = forms.CharField(max_length=100)
    image = forms.ImageField(
        label='请上传一张图片:',
    )