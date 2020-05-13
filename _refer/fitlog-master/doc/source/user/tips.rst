==============
常见问题
==============

1.如果在debug阶段，不希望fitlog发生任何作用，那么直接在入口代码处加入fitlog.debug()
就可以让所有的fitlog调用不起任何作用，debug结束再注释掉这一行就可以了。

2.fitlog 默认只有在产生了第一个metric或loss的时候才会创建log文件夹，防止因为其它bug还没运行
到model就崩溃产生大量无意义的log。

3.如果使用了分布式训练，一般只需要主进程记录fitlog就好。这个时候可以通过将非主进程的fitlog设置fitlog.debug()

.. code-block:: python

    import torch
    import fitlog

    if torch.distributed.get_rank()>0:
        fitlog.debug()


4.不要通过多进程使用fitlog，即multiprocessing模块。

5.fitlog.commit()只需要在某个python文件调用就可以了，一般就在入口python文件即可。

6.传入到fitlog的各种参数、metric的名称，请 **避免特殊符号（例如$%!#@空格），请只使用_与各种字母的组合** ，
因为特殊符号可能导致网页端显示不正常。