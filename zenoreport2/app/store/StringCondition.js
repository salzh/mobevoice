/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 2:11 PM
 * To change this template use File | Settings | File Templates.
 */


Ext.define("Zenoreport.store.StringCondition", {
    extend:'Ext.data.Store',
    autoLoad:true,
    constructor:function (cfg) {
        cfg = cfg || {};
        this.callParent([Ext.apply({
            storeId:'StringCondition',
            fields:['name', 'value'],
            data:[
                {name:'Exactly Matches', value:"like 'STR'"},
                {name:'Begins With', value:"like 'STR%'"},
                {name:'Ends With', value:"like '%STR'"},
                {name:'Contians', value:"like '%STR%'"},
                {name:'Not Begins With', value:"not like 'STR%'"},
                {name:'Not Ends With', value:"not like '%STR'"},
                {name:'Not Contians', value:"not like '%STR%'"}
            ]
        }, cfg)])

    }
});