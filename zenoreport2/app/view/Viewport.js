/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 4:54 AM
 * To change this template use File | Settings | File Templates.
 */

Ext.define("Zenoreport.view.Viewport", {
    extend:'Ext.container.Viewport',
    layout:'border',
    defaults:{
        collapsible:true,
        split:true
    },
    items:[
        {
            //title:'Selection',
            region:'south',
            height:220,
            minHeight:220,
            maxHeight:220,
            layout:'hbox',
            id:'selectedColumns',
            xtype:'panel',
            preventHeader:true,
            resizable:false
        },
        {
            xtype:'zenoreporttoolbar',
            region:'north',
            split:false,
            resizable:false,
            collapsible:false,
            header:false
        },
        {
            title:'Main Content',
            collapsible:false,
            region:'center',
            margins:'5 0 0 0',
            id:'zenoreportBody',
            xtype:'container'
        }
    ]
});
