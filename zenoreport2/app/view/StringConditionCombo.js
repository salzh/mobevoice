/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 2:14 PM
 * To change this template use File | Settings | File Templates.
 */


Ext.define("Zenoreport.view.StringConditionCombo", {
    extend:'Ext.container.Container',
    layout:'hbox',
    alias: 'widget.stringconditioncombo',
    autoRender:true,
    width:320,
    items:[
        {
            xtype:'combo',
            store:'StringCondition',
            displayField:'name',
            valueField:'value',
            emptyText:'Condition',
            width:80,
            queryMode:'local'
        },
        {
            xtype:'textfield',
            emptyText:'string'
        }
    ]

});