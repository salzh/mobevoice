/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 2:30 PM
 * To change this template use File | Settings | File Templates.
 */

Ext.define("Zenoreport.model.Relation", {
    extend:'Ext.data.Model',
    fields:[
        {name:'es', type:'string', mapping:'From Table'},
        {name:'fs', type:'string', mapping:'From Column'},
        {name:'et', type:'string', mapping:'To Table'},
        {name:'ft', type:'string', mapping:'To Column'}
    ]
});