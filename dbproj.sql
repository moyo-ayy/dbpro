PGDMP                     	    {           dbproj    15.4    15.4                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16438    dbproj    DATABASE     h   CREATE DATABASE dbproj WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';
    DROP DATABASE dbproj;
                postgres    false            �            1259    16456    games    TABLE     �   CREATE TABLE public.games (
    date timestamp without time zone,
    location character varying(50),
    leftteamscore integer,
    rightteamscore integer,
    gid integer NOT NULL
);
    DROP TABLE public.games;
       public         heap    postgres    false            �            1259    16444    players    TABLE     �   CREATE TABLE public.players (
    name character varying(50),
    pace integer,
    shooting integer,
    passing integer,
    dribbling integer,
    defending integer,
    physicality integer,
    overall integer,
    pid integer NOT NULL
);
    DROP TABLE public.players;
       public         heap    postgres    false            �            1259    16453    teams    TABLE     �   CREATE TABLE public.teams (
    name character varying(50),
    league character varying(100),
    atkrating integer,
    mdrating integer,
    dfrating integer,
    overall integer,
    tid integer NOT NULL
);
    DROP TABLE public.teams;
       public         heap    postgres    false                      0    16456    games 
   TABLE DATA           S   COPY public.games (date, location, leftteamscore, rightteamscore, gid) FROM stdin;
    public          postgres    false    216   �       
          0    16444    players 
   TABLE DATA           q   COPY public.players (name, pace, shooting, passing, dribbling, defending, physicality, overall, pid) FROM stdin;
    public          postgres    false    214   �                 0    16453    teams 
   TABLE DATA           Z   COPY public.teams (name, league, atkrating, mdrating, dfrating, overall, tid) FROM stdin;
    public          postgres    false    215   �       {           2606    16460    games games_pkey 
   CONSTRAINT     O   ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (gid);
 :   ALTER TABLE ONLY public.games DROP CONSTRAINT games_pkey;
       public            postgres    false    216            w           2606    16448    players players_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_pkey PRIMARY KEY (pid);
 >   ALTER TABLE ONLY public.players DROP CONSTRAINT players_pkey;
       public            postgres    false    214            y           2606    16462    teams teams_pkey 
   CONSTRAINT     O   ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (tid);
 :   ALTER TABLE ONLY public.teams DROP CONSTRAINT teams_pkey;
       public            postgres    false    215                  x������ � �      
      x������ � �            x������ � �     