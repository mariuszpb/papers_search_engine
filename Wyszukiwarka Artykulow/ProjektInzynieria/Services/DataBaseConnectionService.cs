using Microsoft.Data.Sqlite;
using System;
using System.Data.SQLite;
using System.IO;

namespace ProjektInzynieria.Services
{
    public class DataBaseConnectionService
    {
        private readonly string _connectionString;

        public DataBaseConnectionService()
        {
            var dbPath = Path.Combine(AppContext.BaseDirectory, "DataBaseInz.db");

            _connectionString = $"Data Source={dbPath};Version=3;";

            if (!File.Exists(dbPath))
            {
                throw new FileNotFoundException($"Baza danych nie została znaleziona: {dbPath}");
            }
        }

        public SQLiteConnection GetOpenConnection()
        {
            var connection = new SQLiteConnection(_connectionString);
            connection.Open();
            return connection;
        }
    }
}