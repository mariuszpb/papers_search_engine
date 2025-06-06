using Microsoft.AspNetCore.Mvc;
using ProjektInzynieria.Models;
using System.Diagnostics;

namespace ProjektInzynieria.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public IActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Index(string userInput)
        {
            ViewData["UserInput"] = userInput;

            var psi = new ProcessStartInfo
            {
                FileName = "python",
                Arguments = $"search.py \"{userInput}\"",
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true,
                WorkingDirectory = AppDomain.CurrentDomain.BaseDirectory
            };

            var articles = new List<ArticleResult>();

            using (var process = Process.Start(psi))
            {
                while (!process.StandardOutput.EndOfStream)
                {
                    string line = process.StandardOutput.ReadLine()?.Trim();
                    if (!string.IsNullOrWhiteSpace(line) && line.Contains("|"))
                    {
                        var parts = line.Split('|');
                        articles.Add(new ArticleResult
                        {
                            Id = int.Parse(parts[0]),
                            Title = parts[1],
                            Link = parts[2]
                        });
                    }
                }

                process.WaitForExit();
            }

            return View(articles);
        }

        public IActionResult Privacy() => View();

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error() =>
            View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
    }
}