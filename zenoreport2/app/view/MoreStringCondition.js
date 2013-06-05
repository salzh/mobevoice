/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 2:16 PM
 * To change this template use File | Settings | File Templates.
 */


Ext.define("Zenoreport.view.MoreStringCondition", {
    extend:'Ext.container.Container',
    layout:'hbox',
    alias: 'widget.morestringcondition',
    autoRender:true,
    items:[
        {
            xtype:'button',
            text:'x',
            handler:function (btn) {
                btn.up("container").destroy();
            }
        },
        {xtype:'andorcombo'},
        {xtype: 'stringconditioncombo'}
    ],
    listeners:{
        afterrender:function (c) {
            c.up("window").doComponentLayout();
        },
        destroy:function (c) {
            if (c.up("window")) {
                c.up("window").doComponentLayout();
            }
        }
    }
});