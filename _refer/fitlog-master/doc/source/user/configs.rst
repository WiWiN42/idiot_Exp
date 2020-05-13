==============
配置文件
==============

fitlog 的配置文件有 **.fitconfig**


.fitconfig
-------------

**.fitconfig** 文件是 fitlog 的配置文件，一般位于 fitlog 项目的根目录下，也可以放置在项目的根目录中的 .fitlog 文件夹内。
**.fitconfig** 中的默认内容如下：

.. code-block:: shell

    [fit_settings]
    watched_rules = *.py

    [log_settings]
    default_log_dir = ./logs
    save_on_first_metric_or_loss = True

``watched_rules`` 配置的是 fitlog 会自动进行 commit 的文件类型，等号后面是一系列用英文逗号 ``,`` 隔开的规则，
每个规则使用 Python 内置的 `fnmatch <https://docs.python.org/3/library/fnmatch.html>`_ 函数来进行匹配。
你可以添加适当的空格来让配置项更加可读，例如： `watched_rules = *.py, *.mat, test_*.bak` 。

``default_log_dir`` 配置的是 fitlog 记录实验日志的目录，默认位于项目根目录下的 **logs** 文件夹。

``save_on_first_metric_or_loss`` 配置的是否在生成第一个 loss 或者 metric 的时才在日志文件夹下创建一个新的文件夹。
默认值为真，这样实验过程中出错或手动终止的实验就不会产生新的文件夹。

default.cfg
-------------

**default.cfg** 是日志文件夹（默认为项目根目录下的 **logs** 文件夹）中的配置文件。您可以复制或改名这个文件，
只要在命令行启动网页服务时指定配置文件即可。各个选项的功能请参考文件中的注释。

.. code-block:: shell

    [frontend_settings]
    # 以下的几个设置主要是用于控制前端的显示
    Ignore_null_value_when_filter=True
    Wrap_display=False
    Pagination=True
    Hide_hidden_columns_when_reorder=False
    # 前端的任何变动都不会尝试更新到服务器，即所有改动不会保存
    Offline=False
    # 是否保存本次前端页面的改动(包括删除,增加,column排序等)。在server关闭时和更改config时会判断
    Save_settings=True
    # row是否是可以通过拖拽交换的，如果可以交换则无法进行复制
    Reorderable_rows=False
    # 当选择revert代码时 revert到的路径: ../<pj_name>-revert 或 ../<pj_name>-revert-<fit_id>
    No_suffix_when_reset=True
    # 是否忽略掉filter_condition中的不存在对应key的log
    Ignore_filter_condition_not_exist_log=True

    [basic_settings]
    # 如果有内容长度超过这个值，在前端就会被用...替代。
    str_max_length=20
    # float的值保留几位小数
    round_to=6
    # 是否在表格中忽略不改变的column
    ignore_unchanged_columns=True

    [data_settings]
    # 在这里的log将不在前端显示出来，但是可以通过display点击出来。建议通过前端选择
    hidden_logs=
    # 在这里的log将在前端删除。建议通过前端选择
    deleted_logs=
    # 可以设置条件，只有满足以下条件的field才会被显示，请通过前端增加filter条件。
    filter_condition=

    [column_settings]
    # 隐藏的column，建议通过前端选择
    hidden_columns=
    # 不需要显示的column，用逗号隔开，不要使用引号。需要将其从父节点一直写到它本身，比如排除meta中的fit_id, 写为meta-fit_id
    exclude_columns=
    # 允许编辑的column
    editable_columns=memo,meta-fit_msg,meta-git_msg
    # column的显示顺序，强烈推荐不要手动更改
    column_order=

    [chart_settings]
    # 在走势图中，每个对象最多显示的点的数量，不要太大，否则前端可能会卡住
    max_points=200
    # 不需要在走势图中显示的column名称
    chart_exclude_columns=
    # 前端间隔秒多久尝试更新一次走势图，不要设置为太小。
    update_every=4
    # 如果前端超过max_no_updates次更新都没有获取到更新的数据，就停止刷新。如果evaluation的时间特别长，可能需要调大这个选项。
    max_no_updates=40