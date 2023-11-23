PGDMP  "                
    {            dbproj    15.4    16.0     &           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            '           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            (           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            )           1262    16555    dbproj    DATABASE     h   CREATE DATABASE dbproj WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';
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
       public         heap    postgres    false                      0    16556    games 
   TABLE DATA           h   COPY public.games (date, location, leftteamscore, rightteamscore, gid, leftteam, rightteam) FROM stdin;
    public          postgres    false    214   �       #          0    16590    managers 
   TABLE DATA           2   COPY public.managers (mid, tid, name) FROM stdin;
    public          postgres    false    218   ?                  0    16559    players 
   TABLE DATA           q   COPY public.players (name, pace, shooting, passing, dribbling, defending, physicality, overall, pid) FROM stdin;
    public          postgres    false    215   \       !          0    16562    playsfor 
   TABLE DATA           8   COPY public.playsfor (pid, tid, "position") FROM stdin;
    public          postgres    false    216   "       "          0    16567    teams 
   TABLE DATA           Z   COPY public.teams (name, league, atkrating, mdrating, dfrating, overall, tid) FROM stdin;
    public          postgres    false    217   �"                  2606    16571    games games_pkey 
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
       public            postgres    false    218            �           2606    16600    games games_leftteam_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_leftteam_fkey FOREIGN KEY (leftteam) REFERENCES public.teams(tid) ON DELETE CASCADE;
 C   ALTER TABLE ONLY public.games DROP CONSTRAINT games_leftteam_fkey;
       public          postgres    false    217    214    3461            �           2606    16605    games games_rightteam_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_rightteam_fkey FOREIGN KEY (rightteam) REFERENCES public.teams(tid) ON DELETE CASCADE;
 D   ALTER TABLE ONLY public.games DROP CONSTRAINT games_rightteam_fkey;
       public          postgres    false    217    214    3461            �           2606    16612     managers managers_tid_foreignkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.managers
    ADD CONSTRAINT managers_tid_foreignkey FOREIGN KEY (tid) REFERENCES public.teams(tid) ON DELETE CASCADE;
 J   ALTER TABLE ONLY public.managers DROP CONSTRAINT managers_tid_foreignkey;
       public          postgres    false    3461    218    217            �           2606    16580    playsfor playsfor_pid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.playsfor
    ADD CONSTRAINT playsfor_pid_fkey FOREIGN KEY (pid) REFERENCES public.players(pid) ON DELETE CASCADE;
 D   ALTER TABLE ONLY public.playsfor DROP CONSTRAINT playsfor_pid_fkey;
       public          postgres    false    216    3457    215            �           2606    16585    playsfor playsfor_tid_fkey    FK CONSTRAINT     v   ALTER TABLE ONLY public.playsfor
    ADD CONSTRAINT playsfor_tid_fkey FOREIGN KEY (tid) REFERENCES public.teams(tid);
 D   ALTER TABLE ONLY public.playsfor DROP CONSTRAINT playsfor_tid_fkey;
       public          postgres    false    3461    217    216               s   x�M�;�0E�z��l����whi詐h(�(��%������N��
L�8�};���w	B)�X5��`�ZI���`�J��;<�6־�u��q���"F���	9���^���s�      #      x������ � �          �  x�MU�n�8<�_��b(J�xۙ5��#�a/�cq�#z)��뷫5IJ|tuUu�>�C�E���"|#��	�����Zބ�Q],s�_<m�k���F^E�g�Z�oD�����W��J幨��ˌu:Jw�t��;���cU�5��2��aF��e0V~RV7e� چ�b��A@yj}Sw�yI5"���^�Iҫ�x5�L�rا�E��m1���t����X�.֑��� 49��
Rky9�4͉�|_�q����"jp���V�Fޔa�g	��,���9[
�:p�Fm�{ZU�K"E�t�!z{����!��m���c|K>L�L�}�0��Q[y��}���@��|���+b:yꞠ=-u�������!~�	��ˇ�.��CƮ����Ͳ��=����4�2>����D����ː�W�i�9����k�g��ʋ�&9(r�@���є1�6���I]�q��Mȏ�S�1��r�jW��[lp+8�y���7�1�#큉'� �!�O��[��8F�rwp}j,����܏������"���Zu���aX��/�Tұ+=O6��I�9uW*Q6�8}&a�=�Fc��m����v �e��]C��F^�Z�!��0�c`9�v����0��7>�.�g�v5��*��4�+����w�P�Ě�4�a-C���I���@�9��ZL+�����1sI8<����̜��S�j�57F�ײ𜣕�����^Pd���Z�(�T����~.�l*8�qb-L��]��/�����1�;$ID!	�J{����i��'pǗp�蕝h���z�!�I��=7ˤ��qEG9�!�9$��r��g������p�Gĵ��Ŝ��*k��x�Ѡ�u��Tƃ�������ύ�h��e5��4�-�w�'�����>TuQK9N��X��Z��h{��R�� <�x      !   �   x�uһ
1��:�0��%ɔ�`�؈FXvQ�}�fw��2S���X���b8�{{��{ ������Sk�/+��O��>����a��6�/��:�4A%�Ug)���/I����
�
ՐRt��(u�:����ε�s�hk��z�m/P+TC�ѩ[ǩ��qv��T�ZC�l��?����["����SW"�q�xv��H�Z��w�0| ��       "   �   x�e̻
�@F��ߧ��d�3u�3`cg��`��d|{���wΘK7����Y����V$�8H��M��d�\n�n��K��������O�b�f���i��M���Z(B�֚�G׺�=n�Dv`Ň�\Ƙ �3�     