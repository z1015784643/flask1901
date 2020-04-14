<template id="app!">
    <template id="hello">
        <div>
            <h1>hello</h1>
        </div>
    </template>
</template>

<script>
Vue.component('hello-component',{
    template:'$hello',
    el:function(){
        return '#hello'
    },
    data:function(){
        return '#app'
    }
})

new Vue({
    el:'#app'

})
</script>

<style>
 
</style>
