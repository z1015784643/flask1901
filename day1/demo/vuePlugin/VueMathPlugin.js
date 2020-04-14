export default{
    install:function(Vue){
        // 平方
        Vue.directive('square',function(el,binding){
            el.innerHTML = Math.pow(binding.value,2)
        });
        // 开方
        Vue.directive('sqrt',function(el,binding){
            el.innerHTML = Math.sqrt(binding.value,2)
        });
        // 把item当做角度，计算sin，cos，tan值
        // sin正弦值
        Vue.directive('sin',function(el,binding){
            el.innerHTML = Math.sin(binding.value,2)
        });
        // cos  余弦值
        Vue.directive('cos',function(el,binding){
            el.innerHTML = Math.cos(binding.value,2)
        });
        // tan  正切值
        Vue.directive('tan',function(el,binding){
            el.innerHTML = Math.tan(binding.value,2)
        });

        Vue.directive('atan',function(el,binding){
            el.innerHTML = Math.atan(binding.value,2)
        });
    }
    
}