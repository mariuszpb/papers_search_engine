using System.Collections.Generic;
using Microsoft.Data.Sqlite;
using ProjektInzynieria.Services;

namespace ProjektInzynieria.Services
{
    public class Article
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public string Link { get; set; }
    }

    public class Word
    {
        public int ArticleId { get; set; }
        public string WordType { get; set; }
        public string WordText { get; set; }
    }

    public class ArticleText
    {
        public int ArticleId { get; set; }
        public string Text { get; set; }
    }

    public class DataBaseOperationsService
    {
        private readonly DataBaseConnectionService _connectionService;

        public DataBaseOperationsService()
        {
            _connectionService = new DataBaseConnectionService();
        }

        public List<Article> GetArticles()
        {
            var list = new List<Article>();

            using var conn = _connectionService.GetOpenConnection();
            using var cmd = conn.CreateCommand();
            cmd.CommandText = "SELECT id, title, link FROM articles;";

            using var reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                list.Add(new Article
                {
                    Id = reader.GetInt32(0),
                    Title = reader.GetString(1),
                    Link = reader.GetString(2)
                });
            }

            return list;
        }

        public void InsertArticle(string title, string link)
        {
            using var conn = _connectionService.GetOpenConnection();
            using var cmd = conn.CreateCommand();
            cmd.CommandText = "INSERT INTO articles (title, link) VALUES (@title, @link);";
            cmd.Parameters.AddWithValue("@title", title);
            cmd.Parameters.AddWithValue("@link", link);
            cmd.ExecuteNonQuery();
        }

        public void UpdateArticle(int id, string newTitle, string newLink)
        {
            using var conn = _connectionService.GetOpenConnection();
            using var cmd = conn.CreateCommand();
            cmd.CommandText = "UPDATE articles SET title = @title, link = @link WHERE id = @id;";
            cmd.Parameters.AddWithValue("@title", newTitle);
            cmd.Parameters.AddWithValue("@link", newLink);
            cmd.Parameters.AddWithValue("@id", id);
            cmd.ExecuteNonQuery();
        }

        public void DeleteArticle(int id)
        {
            using var conn = _connectionService.GetOpenConnection();
            using var cmd = conn.CreateCommand();
            cmd.CommandText = "DELETE FROM articles WHERE id = @id;";
            cmd.Parameters.AddWithValue("@id", id);
            cmd.ExecuteNonQuery();
        }
    }
}