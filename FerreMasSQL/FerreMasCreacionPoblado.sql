
/****** Object:  Database [FerremasDB]    Script Date: 21-07-2024 2:21:41 ******/


/****** Object:  Table [dbo].[__EFMigrationsHistory]    Script Date: 21-07-2024 2:21:42 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[__EFMigrationsHistory](
	[MigrationId] [nvarchar](150) NOT NULL,
	[ProductVersion] [nvarchar](32) NOT NULL,
 CONSTRAINT [PK___EFMigrationsHistory] PRIMARY KEY CLUSTERED 
(
	[MigrationId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Boleta]    Script Date: 21-07-2024 2:21:42 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Boleta](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Total] [int] NOT NULL,
	[ClienteId] [int] NOT NULL,
	[ProductoId] [int] NOT NULL,
 CONSTRAINT [PK_Boleta] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Cliente]    Script Date: 21-07-2024 2:21:42 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Cliente](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[NombreCliente] [nvarchar](max) NOT NULL,
	[Email] [nvarchar](max) NOT NULL,
	[Telefono] [nvarchar](max) NOT NULL,
 CONSTRAINT [PK_Cliente] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Producto]    Script Date: 21-07-2024 2:21:42 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Producto](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[NombreProducto] [nvarchar](max) NOT NULL,
	[Descripcion] [nvarchar](max) NOT NULL,
	[Precio] [int] NOT NULL,
	[Stock] [int] NOT NULL,
 CONSTRAINT [PK_Producto] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
INSERT [dbo].[__EFMigrationsHistory] ([MigrationId], [ProductVersion]) VALUES (N'20240719172550_Supreme', N'8.0.7')
GO
SET IDENTITY_INSERT [dbo].[Boleta] ON 

INSERT [dbo].[Boleta] ([Id], [Total], [ClienteId], [ProductoId]) VALUES (1, 666666, 1, 2)
SET IDENTITY_INSERT [dbo].[Boleta] OFF
GO
SET IDENTITY_INSERT [dbo].[Cliente] ON 

INSERT [dbo].[Cliente] ([Id], [NombreCliente], [Email], [Telefono]) VALUES (1, N'victor', N'victor@gmail.com', N'45656772')
SET IDENTITY_INSERT [dbo].[Cliente] OFF
GO
SET IDENTITY_INSERT [dbo].[Producto] ON 

INSERT [dbo].[Producto] ([Id], [NombreProducto], [Descripcion], [Precio], [Stock]) VALUES (2, N'Sierra Circular', N'Sierra Circular Profesional De Alto Rendimiento', 666666, 6)
SET IDENTITY_INSERT [dbo].[Producto] OFF
GO
/****** Object:  Index [IX_Boleta_ClienteId]    Script Date: 21-07-2024 2:21:42 ******/
CREATE NONCLUSTERED INDEX [IX_Boleta_ClienteId] ON [dbo].[Boleta]
(
	[ClienteId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IX_Boleta_ProductoId]    Script Date: 21-07-2024 2:21:42 ******/
CREATE NONCLUSTERED INDEX [IX_Boleta_ProductoId] ON [dbo].[Boleta]
(
	[ProductoId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Boleta]  WITH CHECK ADD  CONSTRAINT [FK_Boleta_Cliente_ClienteId] FOREIGN KEY([ClienteId])
REFERENCES [dbo].[Cliente] ([Id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[Boleta] CHECK CONSTRAINT [FK_Boleta_Cliente_ClienteId]
GO
ALTER TABLE [dbo].[Boleta]  WITH CHECK ADD  CONSTRAINT [FK_Boleta_Producto_ProductoId] FOREIGN KEY([ProductoId])
REFERENCES [dbo].[Producto] ([Id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[Boleta] CHECK CONSTRAINT [FK_Boleta_Producto_ProductoId]

ALTER DATABASE [FerreMasDataBase] SET  READ_WRITE 
GO
