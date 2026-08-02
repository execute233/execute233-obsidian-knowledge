启动server比较简单  
import (  
"fmt"  
"io"  
"net/http"  
)  
func Index(writer http.ResponseWriter, request *http.Request) {  
fmt.Println(request.Method, request.URL.String()) // 请求类型，路径  
if request.Method != "GET" {  
bytes, _ := io.ReadAll(request.Body)  
fmt.Println(string(bytes))  
}  
fmt.Println(request.Header)  
writer.Write([]byte("Hello World!")) // 返回结果  
}  
func main() {  
http.HandleFunc("/index", Index)  
fmt.Println("http server is running")  
http.ListenAndServe(":8080", nil)  
}