# ControllerAdvice之@InitBinder

ControllerAdvice功能
对所有的Controller增强，有下面
@ExceptionHandler 抛出异常处理
@ModelAttribute 返回值作为Model数据补充到Controller执行过程中
@InitBinder 补充自定义类型转换器
加在@ControllerAdvice是全局的，加在@Controller是局部的
(WebDataBinder)