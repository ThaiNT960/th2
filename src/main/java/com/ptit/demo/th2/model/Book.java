package com.ptit.demo.th2.model;

public class Book {
    private String bookcode;
    private String title;
    private String author;
    private String category;

    public Book() {
    }

    public Book(String bookcode, String title, String author, String category) {
        this.bookcode = bookcode;
        this.title = title;
        this.author = author;
        this.category = category;
    }

    public String getBookcode() {
        return bookcode;
    }

    public void setBookcode(String bookcode) {
        this.bookcode = bookcode;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }
}
