<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Nhập Sách Thư Viện</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h2 { margin-bottom: 20px; }
        table { border-collapse: collapse; }
        td { padding: 6px 10px; }
        input, select { padding: 4px; width: 250px; }
        .error { color: red; font-size: 13px; }
        .btn { padding: 6px 20px; margin-right: 8px; cursor: pointer; }
    </style>
</head>
<body>
    <h2>Nhập Sách Thư Viện</h2>

    <form action="${pageContext.request.contextPath}/book" method="post">
        <input type="hidden" name="action" value="add">
        <table>
            <tr>
                <td>Book Code:</td>
                <td><input type="text" name="bookcode" value="${bookcode != null ? bookcode : ''}"></td>
                <td><c:if test="${bookcodeError != null}"><span class="error">${bookcodeError}</span></c:if></td>
            </tr>
            <tr>
                <td>Title:</td>
                <td><input type="text" name="title" value="${title != null ? title : ''}"></td>
                <td><c:if test="${titleError != null}"><span class="error">${titleError}</span></c:if></td>
            </tr>
            <tr>
                <td>Author:</td>
                <td><input type="text" name="author" value="${author != null ? author : ''}"></td>
                <td><c:if test="${authorError != null}"><span class="error">${authorError}</span></c:if></td>
            </tr>
            <tr>
                <td>Category:</td>
                <td>
                    <%
                        String selectedCategory = (String) request.getAttribute("category");
                        if (selectedCategory == null || selectedCategory.isEmpty()) {
                            selectedCategory = (String) request.getAttribute("lastCategory");
                        }
                        if (selectedCategory == null) selectedCategory = "";
                    %>
                    <select name="category">
                        <option value="" <%= "".equals(selectedCategory) ? "selected" : "" %>>-- Chọn thể loại --</option>
                        <option value="Khoa học" <%= "Khoa học".equals(selectedCategory) ? "selected" : "" %>>Khoa học</option>
                        <option value="Văn học" <%= "Văn học".equals(selectedCategory) ? "selected" : "" %>>Văn học</option>
                        <option value="Lịch sử" <%= "Lịch sử".equals(selectedCategory) ? "selected" : "" %>>Lịch sử</option>
                        <option value="Công nghệ" <%= "Công nghệ".equals(selectedCategory) ? "selected" : "" %>>Công nghệ</option>
                        <option value="Kinh tế" <%= "Kinh tế".equals(selectedCategory) ? "selected" : "" %>>Kinh tế</option>
                        <option value="Tâm lý" <%= "Tâm lý".equals(selectedCategory) ? "selected" : "" %>>Tâm lý</option>
                        <option value="Thiếu nhi" <%= "Thiếu nhi".equals(selectedCategory) ? "selected" : "" %>>Thiếu nhi</option>
                        <option value="Giáo trình" <%= "Giáo trình".equals(selectedCategory) ? "selected" : "" %>>Giáo trình</option>
                    </select>
                </td>
                <td><c:if test="${categoryError != null}"><span class="error">${categoryError}</span></c:if></td>
            </tr>
            <tr>
                <td></td>
                <td>
                    <button type="submit" class="btn">Add</button>
                    <button type="reset" class="btn">Reset</button>
                </td>
            </tr>
        </table>
    </form>
</body>
</html>
