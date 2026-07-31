# JDBC-SQL注入

为了防止SQL注入，可使用PreparedStatement
PreparedStatement st = connection.prepareStatement("select * from account where name = ? and password = ?")
// 可以填充数据
st.setString(1, name);
st.setString(2, password);
// 然后直接执行
st.executeQuery();