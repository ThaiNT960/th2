<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Xác Nhận Thông Tin Sách</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h2 { margin-bottom: 20px; }
        table { border-collapse: collapse; margin-bottom: 20px; }
        td { padding: 6px 10px; }
        .label { font-weight: bold; }
        .btn { padding: 6px 20px; margin-right: 8px; cursor: pointer; }
        .error { color: red; margin-bottom: 10px; }
    </style>
</head>
<body>
    <h2>Xác Nhận Thông Tin Sách</h2>

    <c:if test="${errorMessage != null}">
        <p class="error">${errorMessage}</p>
    </c:if>

    <table>
        <tr>
            <td class="label">Book Code:</td>
            <td>${book.bookcode}</td>
        </tr>
        <tr>
            <td class="label">Title:</td>
            <td>${book.title}</td>
        </tr>
        <tr>
            <td class="label">Author:</td>
            <td>${book.author}</td>
        </tr>
        <tr>
            <td class="label">Category:</td>
            <td>${book.category}</td>
        </tr>
    </table>

    <form action="${pageContext.request.contextPath}/book" method="post" style="display:inline;">
        <input type="hidden" name="action" value="confirm">
        <input type="hidden" name="bookcode" value="${book.bookcode}">
        <input type="hidden" name="title" value="${book.title}">
        <input type="hidden" name="author" value="${book.author}">
        <input type="hidden" name="category" value="${book.category}">
        <button type="submit" class="btn">Confirm</button>
    </form>
    <form action="${pageContext.request.contextPath}/book" method="post" style="display:inline;">
        <input type="hidden" name="action" value="back">
        <button type="submit" class="btn">Back</button>
    </form>
</body>
</html>
