PGDMP              
    
    {            dbproj    15.4    16.0                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16438    dbproj    DATABASE     h   CREATE DATABASE dbproj WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';
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
       public         heap    postgres    false            �            1259    16495    playsfor    TABLE     j   CREATE TABLE public.playsfor (
    pid integer NOT NULL,
    tid integer NOT NULL,
    "position" text
);
    DROP TABLE public.playsfor;
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
       public         heap    postgres    false                      0    16456    games 
   TABLE DATA           S   COPY public.games (date, location, leftteamscore, rightteamscore, gid) FROM stdin;
    public          postgres    false    216   �                 0    16444    players 
   TABLE DATA           q   COPY public.players (name, pace, shooting, passing, dribbling, defending, physicality, overall, pid) FROM stdin;
    public          postgres    false    214   L                 0    16495    playsfor 
   TABLE DATA           8   COPY public.playsfor (pid, tid, "position") FROM stdin;
    public          postgres    false    217   v                 0    16453    teams 
   TABLE DATA           Z   COPY public.teams (name, league, atkrating, mdrating, dfrating, overall, tid) FROM stdin;
    public          postgres    false    215   �       �           2606    16460    games games_pkey 
   CONSTRAINT     O   ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (gid);
 :   ALTER TABLE ONLY public.games DROP CONSTRAINT games_pkey;
       public            postgres    false    216            {           2606    16448    players players_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_pkey PRIMARY KEY (pid);
 >   ALTER TABLE ONLY public.players DROP CONSTRAINT players_pkey;
       public            postgres    false    214            �           2606    16501    playsfor playsfor_pk 
   CONSTRAINT     X   ALTER TABLE ONLY public.playsfor
    ADD CONSTRAINT playsfor_pk PRIMARY KEY (pid, tid);
 >   ALTER TABLE ONLY public.playsfor DROP CONSTRAINT playsfor_pk;
       public            postgres    false    217    217            }           2606    16462    teams teams_pkey 
   CONSTRAINT     O   ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (tid);
 :   ALTER TABLE ONLY public.teams DROP CONSTRAINT teams_pkey;
       public            postgres    false    215                       2606    16513    teams unique_name 
   CONSTRAINT     L   ALTER TABLE ONLY public.teams
    ADD CONSTRAINT unique_name UNIQUE (name);
 ;   ALTER TABLE ONLY public.teams DROP CONSTRAINT unique_name;
       public            postgres    false    215            �           2606    16514    playsfor playsfor_pid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.playsfor
    ADD CONSTRAINT playsfor_pid_fkey FOREIGN KEY (pid) REFERENCES public.players(pid) ON DELETE CASCADE;
 D   ALTER TABLE ONLY public.playsfor DROP CONSTRAINT playsfor_pid_fkey;
       public          postgres    false    3451    217    214            �           2606    16507    playsfor playsfor_tid_fkey    FK CONSTRAINT     v   ALTER TABLE ONLY public.playsfor
    ADD CONSTRAINT playsfor_tid_fkey FOREIGN KEY (tid) REFERENCES public.teams(tid);
 D   ALTER TABLE ONLY public.playsfor DROP CONSTRAINT playsfor_tid_fkey;
       public          postgres    false    217    3453    215               �   x�E�A
�0��u�s��̤���FP���HR�]��� ����"��-d:Ж9������T�/s�ϥ��ͫ�n�!���%g!���J}e�	1�Hde癛�`iCq2^����۽3!�F�����$�           x�-P�j�0=K_�/(q/�L:-��z��d�Č�[;)��WJ��-=���m�Kbu��`[Ph�i�6�0H��r�E�.�biɀ�A�r���ŋw���M�}L;�B�f1��7���0��^2〟��8)a�9�Ѽ��dXP��k�b��W���C,�&�WW�]����g�d�۳I�Z�+>Fڊn	��J��>�I�ǲ�,ξ$2O�D�1iP�/RJ<�%�-P��%ܪO`I1J���H�� [��~v��^_n����������s_�         \   x�3�4�4027564�tIMK�KI-�2�&h�$螟����Z 6Ŧ�I�73%-35$l�]��0��w,)IL��b5�*j�M4F��� u�>�         `   x�]�1@0���)������Zf4:M�RHAnO�o��b~0�zD=�^�v+<C,ā��ڷ�24���z��M)f]�M���`]�umMsID/b�4     