using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Security.Cryptography;
using System.Text;

namespace ReadChunks
{
    class Program
    {

        static string SERVER = "www.xxxx.com";
        static int SERVER_PORT = 8443;
        static int CONNECT_PORT = 8443;
        static string PASSWORD = "xxx123!1324.0.01";
        /*
        public static byte[] GenerateRandomSalt()
        {
            byte[] data = new byte[32];

            using (RNGCryptoServiceProvider rng = new RNGCryptoServiceProvider())
            {
                for (int i = 0; i < 10; i++)
                {
                    // Fille the buffer with the generated data
                    rng.GetBytes(data);
                }
            }

            return data;
        }*/

        public static byte[] GenerateRandomSalt()
        {
            byte[] data = { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, };
                        
            return data;
        }

        private static string FileEncrypt(string inputFile, string password)
        {      
            //generate random salt
            byte[] salt = GenerateRandomSalt();

            string encryptedFileName = inputFile + ".aes";
            //create output file name
            FileStream fsCrypt = new FileStream(encryptedFileName, FileMode.Create);

            //convert password string to byte arrray
            byte[] passwordBytes = System.Text.Encoding.UTF8.GetBytes(password);

            //Set Rijndael symmetric encryption algorithm
            RijndaelManaged AES = new RijndaelManaged();
            AES.KeySize = 256;
            AES.BlockSize = 128;
            AES.Padding = PaddingMode.PKCS7;
                      
            var key = new Rfc2898DeriveBytes(passwordBytes, salt, 50000);
            AES.Key = key.GetBytes(AES.KeySize / 8);
            AES.IV = key.GetBytes(AES.BlockSize / 8);

          
            AES.Mode = CipherMode.CFB;

            // write salt to the begining of the output file, so in this case can be random every time
            fsCrypt.Write(salt, 0, salt.Length);

            CryptoStream cs = new CryptoStream(fsCrypt, AES.CreateEncryptor(), CryptoStreamMode.Write);

            FileStream fsIn = new FileStream(inputFile, FileMode.Open);

            //create a buffer (1mb) so only this amount will allocate in the memory and not the whole file
            byte[] buffer = new byte[1048576];
            int read;

            try
            {
                while ((read = fsIn.Read(buffer, 0, buffer.Length)) > 0)
                {                    
                    cs.Write(buffer, 0, read);
                }
                               
                fsIn.Close();
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error: " + ex.Message);
            }
            finally
            {
                cs.Close();
                fsCrypt.Close();
            }

            return encryptedFileName;
        }

        private static void FileDecrypt(string inputFile, string outputFile, string password)
        {
            byte[] passwordBytes = System.Text.Encoding.UTF8.GetBytes(password);
            byte[] salt = new byte[32];

            FileStream fsCrypt = new FileStream(inputFile, FileMode.Open);
            fsCrypt.Read(salt, 0, salt.Length);

            RijndaelManaged AES = new RijndaelManaged();
            AES.KeySize = 256;
            AES.BlockSize = 128;
            var key = new Rfc2898DeriveBytes(passwordBytes, salt, 50000);
            AES.Key = key.GetBytes(AES.KeySize / 8);
            AES.IV = key.GetBytes(AES.BlockSize / 8);
            AES.Padding = PaddingMode.PKCS7;
            AES.Mode = CipherMode.CFB;

            CryptoStream cs = new CryptoStream(fsCrypt, AES.CreateDecryptor(), CryptoStreamMode.Read);

            FileStream fsOut = new FileStream(outputFile, FileMode.Create);

            int read;
            byte[] buffer = new byte[1048576];

            try
            {
                while ((read = cs.Read(buffer, 0, buffer.Length)) > 0)
                {                   
                    fsOut.Write(buffer, 0, read);
                }
            }
            catch (CryptographicException ex_CryptographicException)
            {
                Console.WriteLine("CryptographicException error: " + ex_CryptographicException.Message);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error: " + ex.Message);
            }

            try
            {
                cs.Close();
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error by closing CryptoStream: " + ex.Message);
            }
            finally
            {
                fsOut.Close();
                fsCrypt.Close();
            }
        }

        public static void connect_and_send(String server, Int32 port, String FileName)
        {
            try
            {                             
                TcpClient client = new TcpClient(server, port);

                NetworkStream stream = client.GetStream();

                const int chunkSize = 1024 * 1024; // read the file by chunks of 1MB
                using (var file = File.OpenRead(FileName))
                {
                    int bytesRead;
                    var buffer = new byte[chunkSize];
                    while ((bytesRead = file.Read(buffer, 0, buffer.Length)) > 0)
                    {
                        stream.Write(buffer, 0, bytesRead);
                    }
                }            

                stream.Close();
                client.Close();
            }
            catch (ArgumentNullException e)
            {
                Console.WriteLine("ArgumentNullException: {0}", e);
            }
            catch (SocketException e)
            {
                Console.WriteLine("SocketException: {0}", e);
            }          
        }

        public static void listen_and_receive(Int32 port, string filename)
        {

            TcpListener server = null;
            try
            {
                IPAddress localAddr = IPAddress.Parse("0.0.0.0");

                // TcpListener server = new TcpListener(port);
                server = new TcpListener(localAddr, port);

                // Start listening for client requests.
                server.Start();

                // Enter the listening loop.

                Console.Write("Waiting for a connection... ");

                // Perform a blocking call to accept requests.
                // You could also use server.AcceptSocket() here.
                TcpClient client = server.AcceptTcpClient();
                Console.WriteLine("Connected!");

                // Get a stream object for reading and writing
                NetworkStream stream = client.GetStream();

                int bytesRead;
                const int chunkSize = 1024 * 1024; // read the file by chunks of 1MB
                Byte[] bytes = new Byte[chunkSize];
                using (var file = File.OpenWrite(filename))
                {
                    while ((bytesRead = stream.Read(bytes, 0, bytes.Length)) != 0)
                    {
                        file.Write(bytes, 0, bytesRead);
                    }
                }

                // Shutdown and end connection
                stream.Close();
                client.Close();

            }
            catch (SocketException e)
            {
                Console.WriteLine("SocketException: {0}", e);
            }
            finally
            {
                // Stop listening for new clients.
                server.Stop();
            }

        }

        public static void Execute(String FileName)
        {
            string newfilename = FileEncrypt(FileName, PASSWORD);
            connect_and_send(SERVER, CONNECT_PORT, newfilename);
        }
           
        public static void Main(string[] args)
        {
            // listen / upload | port            
            if (args.Length < 1) 
            {
                Console.WriteLine("Usage: ");
                return;
            }

            int port = SERVER_PORT;            
            string operation = args[0];
            //port = Int32.Parse(args[0]);
            if (operation.ToLower() == "listen")
            {
                listen_and_receive(port, "encrypted.file");
                FileDecrypt("encrypted.file", "decrypted", PASSWORD);
            } else if (operation.ToLower() == "upload")
            {
                Execute(args[1]);
            }
        }
    }
}
