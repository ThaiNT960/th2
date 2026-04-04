package com.ptit.demo.th2.servlet;

import com.ptit.demo.th2.dao.BookDAO;
import com.ptit.demo.th2.model.Book;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@WebServlet(name = "bookServlet", value = "/book")
public class BookServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        // Lấy category từ session nếu có
        HttpSession session = request.getSession();
        String savedCategory = (String) session.getAttribute("lastCategory");
        if (savedCategory != null) {
            request.setAttribute("lastCategory", savedCategory);
        }
        request.getRequestDispatcher("/bookForm.jsp").forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        request.setCharacterEncoding("UTF-8");
        String action = request.getParameter("action");

        if ("add".equals(action)) {
            handleAdd(request, response);
        } else if ("confirm".equals(action)) {
            handleConfirm(request, response);
        } else if ("back".equals(action)) {
            // Quay lại form nhập
            response.sendRedirect(request.getContextPath() + "/book");
        } else {
            response.sendRedirect(request.getContextPath() + "/book");
        }
    }

    private void handleAdd(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String bookcode = request.getParameter("bookcode");
        String title = request.getParameter("title");
        String author = request.getParameter("author");
        String category = request.getParameter("category");

        // Validate
        Map<String, String> errors = new HashMap<>();

        if (bookcode == null || bookcode.trim().isEmpty()) {
            errors.put("bookcodeError", "Book code không được để trống");
        } else if (BookDAO.isBookcodeExists(bookcode.trim())) {
            errors.put("bookcodeError", "Book code đã tồn tại trong CSDL");
        }

        if (title == null || title.trim().isEmpty()) {
            errors.put("titleError", "Title không được để trống");
        }

        if (author == null || author.trim().isEmpty()) {
            errors.put("authorError", "Author không được để trống");
        }

        if (category == null || category.trim().isEmpty() || "".equals(category)) {
            errors.put("categoryError", "Category không được để trống");
        }

        if (!errors.isEmpty()) {
            // Có lỗi, quay lại form với thông báo lỗi
            for (Map.Entry<String, String> entry : errors.entrySet()) {
                request.setAttribute(entry.getKey(), entry.getValue());
            }
            request.setAttribute("bookcode", bookcode);
            request.setAttribute("title", title);
            request.setAttribute("author", author);
            request.setAttribute("category", category);

            // Lấy lastCategory từ session
            HttpSession session = request.getSession();
            String savedCategory = (String) session.getAttribute("lastCategory");
            if (savedCategory != null && (category == null || category.trim().isEmpty())) {
                request.setAttribute("lastCategory", savedCategory);
            }

            request.getRequestDispatcher("/bookForm.jsp").forward(request, response);
            return;
        }

        // Không có lỗi, lưu category vào session và chuyển đến trang xác nhận
        HttpSession session = request.getSession();
        session.setAttribute("lastCategory", category.trim());

        // Lưu thông tin sách vào request để hiển thị trên trang xác nhận
        Book book = new Book(bookcode.trim(), title.trim(), author.trim(), category.trim());
        request.setAttribute("book", book);
        request.getRequestDispatcher("/bookConfirm.jsp").forward(request, response);
    }

    private void handleConfirm(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String bookcode = request.getParameter("bookcode");
        String title = request.getParameter("title");
        String author = request.getParameter("author");
        String category = request.getParameter("category");

        Book book = new Book(bookcode, title, author, category);
        boolean success = BookDAO.insertBook(book);

        if (success) {
            // Thêm thành công, quay lại form nhập
            HttpSession session = request.getSession();
            session.setAttribute("lastCategory", category);
            response.sendRedirect(request.getContextPath() + "/book");
        } else {
            request.setAttribute("errorMessage", "Lỗi khi thêm sách vào CSDL!");
            request.setAttribute("book", book);
            request.getRequestDispatcher("/bookConfirm.jsp").forward(request, response);
        }
    }
}
