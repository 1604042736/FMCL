<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="zh_CN">
<context>
    <name>CustomFunction</name>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="230"/>
        <source>自定义功能</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="231"/>
        <source>请先看完&quot;开发者&quot;帮助后再看本页面</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="232"/>
        <source>如果有不清楚的可以去FMCL/Functions或FMCL/Default/FMCL/Functions下看看已有的功能是如何实现的</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="233"/>
        <source>步骤3：编写功能</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="234"/>
        <source>准备工作已做完，可以开始进行真正的功能开发了</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="235"/>
        <source>实际上步骤2和步骤3不一定要依次进行</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="236"/>
        <source>步骤1：创建功能</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="237"/>
        <source>在FMCL/Functions中创建文件夹，文件夹名称自取</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="238"/>
        <source>在该文件夹下创建__init__.py</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="239"/>
        <source>步骤2：编写对外函数</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="240"/>
        <source>defaultSetting和defaultSettingAttr</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="241"/>
        <source>以下是这两个函数的基本模板</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="242"/>
        <source>该功能的设置和设置属性</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="243"/>
        <source>对于每个设置中的每个子项都必须要有对应的属性</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="244"/>
        <source>&lt;!DOCTYPE HTML PUBLIC &quot;-//W3C//DTD HTML 4.0//EN&quot; &quot;http://www.w3.org/TR/REC-html40/strict.dtd&quot;&gt;
&lt;html&gt;&lt;head&gt;&lt;meta name=&quot;qrichtext&quot; content=&quot;1&quot; /&gt;&lt;meta charset=&quot;utf-8&quot; /&gt;&lt;style type=&quot;text/css&quot;&gt;
p, li { white-space: pre-wrap; }
hr { height: 1px; border-width: 0; }
li.unchecked::marker { content: &quot;\2610&quot;; }
li.checked::marker { content: &quot;\2612&quot;; }
&lt;/style&gt;&lt;/head&gt;&lt;body style=&quot; font-family:&apos;Segoe UI&apos;,&apos;Microsoft YaHei&apos;,&apos;PingFang SC&apos;; font-size:14px; font-weight:400; font-style:normal;&quot;&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px;&quot;&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#af00db;&quot;&gt;from&lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#3b3b3b;&quot;&gt; &lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#267f99;&quot;&gt;Setting&lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#3b3b3b;&quot;&gt; &lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#af00db;&quot;&gt;import&lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#3b3b3b;&quot;&gt; &lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#267f99;&quot;&gt;SettingAttr&lt;/span&gt;&lt;/p&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#0000ff;&quot;&gt;def&lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#3b3b3b;&quot;&gt; &lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#795e26;&quot;&gt;defaultSetting&lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#3b3b3b;&quot;&gt;():&lt;/span&gt;&lt;/p&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#3b3b3b;&quot;&gt;    &lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#af00db;&quot;&gt;return&lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#3b3b3b;&quot;&gt; {}&lt;/span&gt;&lt;/p&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#0000ff;&quot;&gt;def&lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#3b3b3b;&quot;&gt; &lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#795e26;&quot;&gt;defaultSettingAttr&lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#3b3b3b;&quot;&gt;() -&amp;gt; &lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#267f99;&quot;&gt;dict&lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#3b3b3b;&quot;&gt;[&lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#267f99;&quot;&gt;str&lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#3b3b3b;&quot;&gt;, &lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#267f99;&quot;&gt;SettingAttr&lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#3b3b3b;&quot;&gt;]:&lt;/span&gt;&lt;/p&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#3b3b3b;&quot;&gt;    &lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#af00db;&quot;&gt;return&lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#3b3b3b;&quot;&gt; {}&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="256"/>
        <source>比如对于a.b.c，必须要有a, a.b, a.b.c的设置属性</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="257"/>
        <source>functionInfo</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="258"/>
        <source>&lt;!DOCTYPE HTML PUBLIC &quot;-//W3C//DTD HTML 4.0//EN&quot; &quot;http://www.w3.org/TR/REC-html40/strict.dtd&quot;&gt;
&lt;html&gt;&lt;head&gt;&lt;meta name=&quot;qrichtext&quot; content=&quot;1&quot; /&gt;&lt;meta charset=&quot;utf-8&quot; /&gt;&lt;style type=&quot;text/css&quot;&gt;
p, li { white-space: pre-wrap; }
hr { height: 1px; border-width: 0; }
li.unchecked::marker { content: &quot;\2610&quot;; }
li.checked::marker { content: &quot;\2612&quot;; }
&lt;/style&gt;&lt;/head&gt;&lt;body style=&quot; font-family:'Segoe UI','Microsoft YaHei','PingFang SC'; font-size:14px; font-weight:400; font-style:normal;&quot;&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px;&quot;&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#0000ff;&quot;&gt;def&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt; &lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#795e26;&quot;&gt;functionInfo&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;():&lt;/span&gt;&lt;/p&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;    &lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#af00db;&quot;&gt;return&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt; {&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#a31515;&quot;&gt;&amp;quot;name&amp;quot;&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;: &lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#a31515;&quot;&gt;&amp;quot;功能的名称&amp;quot;&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;, &lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#a31515;&quot;&gt;&amp;quot;id&amp;quot;&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;: &lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#a31515;&quot;&gt;&amp;quot;功能的标识符&amp;quot;&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;, &lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#a31515;&quot;&gt;&amp;quot;icon&amp;quot;&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;: &lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#a31515;&quot;&gt;&amp;quot;功能的图标&amp;quot;&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;}&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="267"/>
        <source>系统获取该功能的信息时调用</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="284"/>
        <source>以下是该函数的基本模板</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="269"/>
        <source>上面的模板返回的是完整的信息，如果有缺少，缺少的信息会由系统设置</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="270"/>
        <source>main</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="271"/>
        <source>&lt;!DOCTYPE HTML PUBLIC &quot;-//W3C//DTD HTML 4.0//EN&quot; &quot;http://www.w3.org/TR/REC-html40/strict.dtd&quot;&gt;
&lt;html&gt;&lt;head&gt;&lt;meta name=&quot;qrichtext&quot; content=&quot;1&quot; /&gt;&lt;meta charset=&quot;utf-8&quot; /&gt;&lt;style type=&quot;text/css&quot;&gt;
p, li { white-space: pre-wrap; }
hr { height: 1px; border-width: 0; }
li.unchecked::marker { content: &quot;\2610&quot;; }
li.checked::marker { content: &quot;\2612&quot;; }
&lt;/style&gt;&lt;/head&gt;&lt;body style=&quot; font-family:&apos;Segoe UI&apos;,&apos;Microsoft YaHei&apos;,&apos;PingFang SC&apos;; font-size:14px; font-weight:400; font-style:normal;&quot;&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px;&quot;&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#0000ff;&quot;&gt;def&lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#3b3b3b;&quot;&gt; &lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#795e26;&quot;&gt;main&lt;/span&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#3b3b3b;&quot;&gt;():&lt;/span&gt;&lt;/p&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-family:&apos;Consolas&apos;,&apos;Courier New&apos;,&apos;monospace&apos;; font-size:9pt; color:#3b3b3b;&quot;&gt;    ...&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="280"/>
        <source>主程序，系统运行该功能时会调用</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="282"/>
        <source>可以有任意参数，但要注意该函数调用时不一定会有参数传进来</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="283"/>
        <source>helpIndex</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="285"/>
        <source>&lt;!DOCTYPE HTML PUBLIC &quot;-//W3C//DTD HTML 4.0//EN&quot; &quot;http://www.w3.org/TR/REC-html40/strict.dtd&quot;&gt;
&lt;html&gt;&lt;head&gt;&lt;meta name=&quot;qrichtext&quot; content=&quot;1&quot; /&gt;&lt;meta charset=&quot;utf-8&quot; /&gt;&lt;style type=&quot;text/css&quot;&gt;
p, li { white-space: pre-wrap; }
hr { height: 1px; border-width: 0; }
li.unchecked::marker { content: &quot;\2610&quot;; }
li.checked::marker { content: &quot;\2612&quot;; }
&lt;/style&gt;&lt;/head&gt;&lt;body style=&quot; font-family:'Segoe UI','Microsoft YaHei','PingFang SC'; font-size:14px; font-weight:400; font-style:normal;&quot;&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px;&quot;&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#0000ff;&quot;&gt;def&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt; &lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#795e26;&quot;&gt;helpIndex&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;():&lt;/span&gt;&lt;/p&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;    &lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#af00db;&quot;&gt;return&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt; {&lt;/span&gt;&lt;/p&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;        &lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#a31515;&quot;&gt;&amp;quot;页面1&amp;quot;&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;: {&lt;/span&gt;&lt;/p&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;            &lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#a31515;&quot;&gt;&amp;quot;name&amp;quot;&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;: &lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#a31515;&quot;&gt;&amp;quot;名称&amp;quot;&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;,&lt;/span&gt;&lt;/p&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;            &lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#a31515;&quot;&gt;&amp;quot;page&amp;quot;&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;: ..., &lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#00821a;&quot;&gt;#&amp;quot;对应的页面(可选)，是一个返回QWidget的函数&lt;/span&gt;&lt;/p&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;            &lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#a31515;&quot;&gt;&amp;quot;子页面1&amp;quot;&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;: {...},&lt;/span&gt;&lt;/p&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;            &lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#a31515;&quot;&gt;&amp;quot;子页面2&amp;quot;&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;: {...},&lt;/span&gt;&lt;/p&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;        },&lt;/span&gt;&lt;/p&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;        &lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#a31515;&quot;&gt;&amp;quot;页面2&amp;quot;&lt;/span&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;: {...},&lt;/span&gt;&lt;/p&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-family:'Consolas','Courier New','monospace'; font-size:9pt; color:#3b3b3b;&quot;&gt;    }&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="302"/>
        <source>该功能的帮助索引</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="303"/>
        <source>每个页面的字典的内容相同，并且该字典的每个键用'.'相连就成了标识符(id)，可以通过id直接获得对应字典的值</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="304"/>
        <source>以下函数都是写在__init__.py中的</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="305"/>
        <source>步骤4：翻译</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="306"/>
        <source>使用PyQt5对应的工具生成功能的翻译.ts文件，并用&quot;语言家&quot;进行翻译，翻译文件应该放在&quot;FMCL/Functions/你创建的文件夹/Translations&quot;下</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomFunction.py" line="307"/>
        <source>翻译文件名必须与语言类型相同，比如简体中文的翻译的文件名是&quot;简体中文.ts&quot;，英文的翻译的文件名是&quot;English.ts&quot;</source>
        <translation></translation>
    </message>
</context>
<context>
    <name>CustomHelp</name>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomHelp.py" line="103"/>
        <source>自定义帮助</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomHelp.py" line="104"/>
        <source>步骤1：创建帮助</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomHelp.py" line="105"/>
        <source>在FMCL/Help文件夹下创建文件夹，文件夹名称自取，并创建__init__.py</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomHelp.py" line="106"/>
        <source>请先看完&quot;开发者&quot;帮助后再看本页面</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomHelp.py" line="107"/>
        <source>步骤3：编写帮助页面</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomHelp.py" line="108"/>
        <source>准备工作已做完，可以开始编写具体的帮助页面了</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomHelp.py" line="109"/>
        <source>实际上步骤2和步骤3不一定要依次进行</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomHelp.py" line="110"/>
        <source>步骤2：编写对外函数</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomHelp.py" line="111"/>
        <source>只需在__init__.py中写helpIndex函数即可，该函数内容与&quot;自定义功能&quot;中提到的helpIndex函数相同</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomHelp.py" line="112"/>
        <source>步骤4：翻译</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_CustomHelp.py" line="113"/>
        <source>同&quot;自定义功能&quot;步骤4，但要注意的是翻译文件要放在&quot;FMCL/Help/你创建的文件夹/Translations&quot;下</source>
        <translation></translation>
    </message>
</context>
<context>
    <name>Developer</name>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_Developer.py" line="67"/>
        <source>开发者</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_Developer.py" line="68"/>
        <source>此帮助页面及其子帮助页面是面向开发者的</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_Developer.py" line="69"/>
        <source>对开发者的基本要求</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_Developer.py" line="70"/>
        <source>1. 会Python</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_Developer.py" line="71"/>
        <source>2. 会PyQt5</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_Developer.py" line="72"/>
        <source>无特殊说明，该帮助页面及其子页面中提到的路径都是以启动器主程序所在目录为根目录</source>
        <translation></translation>
    </message>
</context>
<context>
    <name>DeveloperHelp</name>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/__init__.py" line="16"/>
        <source>开发者</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/__init__.py" line="19"/>
        <source>自定义功能</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/__init__.py" line="23"/>
        <source>自定义帮助</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/__init__.py" line="27"/>
        <source>翻译</source>
        <translation></translation>
    </message>
</context>
<context>
    <name>Translation</name>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_Translation.py" line="50"/>
        <source>翻译</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_Translation.py" line="51"/>
        <source>将翻译文件（&quot;语言家&quot;生成的qm文件）放入&quot;FMCL/Translations&quot;下的一个文件夹即可</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../../../../../������/PCG/FMCL/FMCL/Help/Developer/ui_Translation.py" line="52"/>
        <source>该翻译文件的文件名要与它对应语言类型相符，这与&quot;自定义功能&quot;中的步骤4要求相同</source>
        <translation></translation>
    </message>
</context>
</TS>
