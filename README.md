# xmlTomd
## 说明

用于将博客园备份出的xml文件,将每个文章分别转换成md文件

生成的md文件用于github pages 与 jekyll搭建的个人静态博客

将博客园的数据备份, 生成的xml文件, 放到xml_data文件夹下, 并在xmlTomd.py中输入要转换的文件名

启动
```python
python3 xmlTomd.py
```

转换完成后, 会生成md_data文件夹, 将生成的文件直接放入到git page项目中即可使用