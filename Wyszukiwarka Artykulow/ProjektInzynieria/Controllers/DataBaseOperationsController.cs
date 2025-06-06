using Microsoft.AspNetCore.Mvc;
using ProjektInzynieria.Services;
using ProjektInzynieria.Models;

public class DataBaseOperationsController : Controller
{
    private readonly DataBaseOperationsService _service;

    public DataBaseOperationsController()
    {
        _service = new DataBaseOperationsService();
    }

    public IActionResult Index()
    {
        var articles = _service.GetArticles();
        return View(articles);
    }

    [HttpPost]
    public IActionResult Insert(string title, string link)
    {
        if (!string.IsNullOrWhiteSpace(title) && !string.IsNullOrWhiteSpace(link))
        {
            _service.InsertArticle(title, link);
        }
        return RedirectToAction("Index");
    }

    [HttpPost]
    public IActionResult Update(int id, string title, string link)
    {
        if (id > 0 && !string.IsNullOrWhiteSpace(title) && !string.IsNullOrWhiteSpace(link))
        {
            _service.UpdateArticle(id, title, link);
        }
        return RedirectToAction("Index");
    }

    [HttpPost]
    public IActionResult Delete(int id)
    {
        if (id > 0)
        {
            _service.DeleteArticle(id);
        }
        return RedirectToAction("Index");
    }

    [HttpPost]
    public IActionResult Edit(int id)
    {
        var articles = _service.GetArticles();
        ViewData["EditingId"] = id;
        return View("Index", articles);
    }

    [HttpGet]
    public IActionResult CancelEdit()
    {
        var articles = _service.GetArticles();
        return View("Index", articles);
    }
}