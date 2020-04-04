
function list_group(selection, data, callback){

    var state = []
    for (var i=0; i<data.length; i++){
        state.push(false)
    }

    var updateState = (d, i, parent)=>{        
        if(state[i]){
            d3.select(parent[i]).style('background-color', 'rgb(245, 245, 245)')
        }else{
            d3.select(parent[i]).style('background-color', '#bbf0ca')
        }
        state[i] = !state[i]  
        
        if(callback)
            callback(state, i, d)
    }

    d3.select(selection)
        .selectAll('.list_group_item')
        .data(data)
        .join('div')
        .attr('class', 'list_group_item')
        .on('click', updateState)
        .append('span')
        .text(d => d)

}