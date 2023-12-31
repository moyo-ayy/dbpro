PGDMP  4    )            
    {            dbproj    15.4    16.0     -           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            .           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            /           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            0           1262    16555    dbproj    DATABASE     h   CREATE DATABASE dbproj WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';
    DROP DATABASE dbproj;
                postgres    false            �            1259    16556    games    TABLE     �   CREATE TABLE public.games (
    date timestamp without time zone,
    location character varying(50),
    leftteamscore integer,
    rightteamscore integer,
    gid integer NOT NULL,
    leftteam integer,
    rightteam integer
);
    DROP TABLE public.games;
       public         heap    postgres    false            �            1259    16590    managers    TABLE     m   CREATE TABLE public.managers (
    mid integer NOT NULL,
    tid integer,
    name character varying(255)
);
    DROP TABLE public.managers;
       public         heap    postgres    false            �            1259    16559    players    TABLE     �   CREATE TABLE public.players (
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
       public         heap    postgres    false            �            1259    16562    playsfor    TABLE     j   CREATE TABLE public.playsfor (
    pid integer NOT NULL,
    tid integer NOT NULL,
    "position" text
);
    DROP TABLE public.playsfor;
       public         heap    postgres    false            �            1259    16567    teams    TABLE     �   CREATE TABLE public.teams (
    name character varying(50),
    league character varying(100),
    atkrating integer,
    mdrating integer,
    dfrating integer,
    overall integer,
    tid integer NOT NULL
);
    DROP TABLE public.teams;
       public         heap    postgres    false            �            1259    16622    users    TABLE     �   CREATE TABLE public.users (
    username character varying(50) NOT NULL,
    type character varying(50),
    password character varying(255)
);
    DROP TABLE public.users;
       public         heap    postgres    false            %          0    16556    games 
   TABLE DATA           h   COPY public.games (date, location, leftteamscore, rightteamscore, gid, leftteam, rightteam) FROM stdin;
    public          postgres    false    214   �        )          0    16590    managers 
   TABLE DATA           2   COPY public.managers (mid, tid, name) FROM stdin;
    public          postgres    false    218   R!       &          0    16559    players 
   TABLE DATA           q   COPY public.players (name, pace, shooting, passing, dribbling, defending, physicality, overall, pid) FROM stdin;
    public          postgres    false    215   �!       '          0    16562    playsfor 
   TABLE DATA           8   COPY public.playsfor (pid, tid, "position") FROM stdin;
    public          postgres    false    216   \%       (          0    16567    teams 
   TABLE DATA           Z   COPY public.teams (name, league, atkrating, mdrating, dfrating, overall, tid) FROM stdin;
    public          postgres    false    217   7&       *          0    16622    users 
   TABLE DATA           9   COPY public.users (username, type, password) FROM stdin;
    public          postgres    false    219   �&       �           2606    16571    games games_pkey 
   CONSTRAINT     O   ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (gid);
 :   ALTER TABLE ONLY public.games DROP CONSTRAINT games_pkey;
       public            postgres    false    214            �           2606    16594    managers managers_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public.managers
    ADD CONSTRAINT managers_pkey PRIMARY KEY (mid);
 @   ALTER TABLE ONLY public.managers DROP CONSTRAINT managers_pkey;
       public            postgres    false    218            �           2606    16573    players players_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_pkey PRIMARY KEY (pid);
 >   ALTER TABLE ONLY public.players DROP CONSTRAINT players_pkey;
       public            postgres    false    215            �           2606    16575    playsfor playsfor_pk 
   CONSTRAINT     X   ALTER TABLE ONLY public.playsfor
    ADD CONSTRAINT playsfor_pk PRIMARY KEY (pid, tid);
 >   ALTER TABLE ONLY public.playsfor DROP CONSTRAINT playsfor_pk;
       public            postgres    false    216    216            �           2606    16577    teams teams_pkey 
   CONSTRAINT     O   ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (tid);
 :   ALTER TABLE ONLY public.teams DROP CONSTRAINT teams_pkey;
       public            postgres    false    217            �           2606    16579    teams unique_name 
   CONSTRAINT     L   ALTER TABLE ONLY public.teams
    ADD CONSTRAINT unique_name UNIQUE (name);
 ;   ALTER TABLE ONLY public.teams DROP CONSTRAINT unique_name;
       public            postgres    false    217            �           2606    16611    managers unique_tid 
   CONSTRAINT     M   ALTER TABLE ONLY public.managers
    ADD CONSTRAINT unique_tid UNIQUE (tid);
 =   ALTER TABLE ONLY public.managers DROP CONSTRAINT unique_tid;
       public            postgres    false    218            �           2606    16626    users users_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (username);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    219            �           2606    16600    games games_leftteam_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_leftteam_fkey FOREIGN KEY (leftteam) REFERENCES public.teams(tid) ON DELETE CASCADE;
 C   ALTER TABLE ONLY public.games DROP CONSTRAINT games_leftteam_fkey;
       public          postgres    false    217    3465    214            �           2606    16605    games games_rightteam_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_rightteam_fkey FOREIGN KEY (rightteam) REFERENCES public.teams(tid) ON DELETE CASCADE;
 D   ALTER TABLE ONLY public.games DROP CONSTRAINT games_rightteam_fkey;
       public          postgres    false    3465    217    214            �           2606    16612     managers managers_tid_foreignkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.managers
    ADD CONSTRAINT managers_tid_foreignkey FOREIGN KEY (tid) REFERENCES public.teams(tid) ON DELETE CASCADE;
 J   ALTER TABLE ONLY public.managers DROP CONSTRAINT managers_tid_foreignkey;
       public          postgres    false    218    3465    217            �           2606    16580    playsfor playsfor_pid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.playsfor
    ADD CONSTRAINT playsfor_pid_fkey FOREIGN KEY (pid) REFERENCES public.players(pid) ON DELETE CASCADE;
 D   ALTER TABLE ONLY public.playsfor DROP CONSTRAINT playsfor_pid_fkey;
       public          postgres    false    216    215    3461            �           2606    16585    playsfor playsfor_tid_fkey    FK CONSTRAINT     v   ALTER TABLE ONLY public.playsfor
    ADD CONSTRAINT playsfor_tid_fkey FOREIGN KEY (tid) REFERENCES public.teams(tid);
 D   ALTER TABLE ONLY public.playsfor DROP CONSTRAINT playsfor_tid_fkey;
       public          postgres    false    3465    217    216            %   s   x�M�;�0E�z��l����whi詐h(�(��%������N��
L�8�};���w	B)�X5��`�ZI���`�J��;<�6־�u��q���"F���	9���^���s�      )   ?   x�3�4��4��02�����˫Tp*J,��2�01�41555��,IL�/�T�,������� �      &   �  x�MU�r�6|�?Ў@� �(�Q=vlgO&}A$�D.H�q���G9�������>�C�E���"|#��	�����Zބ�Q],s��x
�k���F^E�G�Z�oD������y��sQW!���(���i�k v��-Ǫv5j�Oe�CV��e2V~RV7e�(چ���@yj}Sw�yI5� q��E���	�Ɯ)*�}
�h��-�sr���u���:R�I ��� �W�Z�ˡ�iN$懚�S�'B���)s$EZ�yS��%���L
/�l	t���ڐ��U})u��N��C��,/1�C�������6�|��L?��i:$M���~��]�����렏�P�^���]�{����1V��Bk���AM(�^>�GuI2�pFE�/���r[O�\���=���D����ː�7�y�9����k���U'M� <�:�A-P�BS���4r{'u�1�3�����Mc���ծL3طp�4�}���7"�)�#��D�k��
y�tT��D�},d��%� YT��D�kK5N>�a��6��R�c�y�*؈�'��X�]��Ǆ��3��Ԙ8����寤��sYf��D�l�u�e�z
c8֚=E��fܡFSg��_��q&lW�h���!^9�6��uJ,��/;�=f �>�=	��45gb��i���@�9f���C����z
Ym��C�I����y�9Z���z��dyR��	��2����s�g��Ǝk���1^~]�x*�`y�Q������9���߉;��'�bv��iY���]�	���<1,��¤���@@�3$l��j�{/�l������Fµ��Ŝ���Y�p�8Р�ێ��t*�A���x.qO��(8h�Z�bM��4�-�y0b൜���>TuQK9N���V�	6��������!�n*��1�h���w)�S�x&      '   �   x�uһ
1��:�0��%ɔ�`�؈FXvQ�}�fw��2S���X���b8�{{��{ ������Sk�/+��O��>����a��6�/��:�4A%�Ug)���/I����
�
ՐRt��(u�:����ε�s�hk��z�m/P+TC�ѩ[ǩ��qv��T�ZC�l��?����["����SW"�q�xv��H�Z��w�0| ��       (   �   x�e�;�0��z�9���[#�D�����K�D� q{\���Ʃt�\�8����i���@-4@N�Do{�q*�{z��N%�t�Δ!��� \d���'�u.[�Ld��X���LCnz���_��{h��G�E���~�~4�      *   �   x�u�Kn!C��a��]p��a6�O��ls�e�H�La?~�ޏ{���w45�^398u$tj��J��ֱ��.��ʮ÷�L��['���vE ��K=���3*�oU�+)f�as�#�2Y�NN���i��2<_�P��F*&�{n�n&��.�����K�7�ΨL��H�J���6Aմ��#Nw��}�e��(`�M����_Y�7���(�� .�\N     