--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0
-- Dumped by pg_dump version 16.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: games; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.games (
    date timestamp without time zone,
    location character varying(50),
    leftteamscore integer,
    rightteamscore integer,
    gid integer NOT NULL
);


ALTER TABLE public.games OWNER TO postgres;

--
-- Name: players; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.players (
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


ALTER TABLE public.players OWNER TO postgres;

--
-- Name: playsfor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.playsfor (
    pid integer NOT NULL,
    tid integer NOT NULL,
    "position" text
);


ALTER TABLE public.playsfor OWNER TO postgres;

--
-- Name: teams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teams (
    name character varying(50),
    league character varying(100),
    atkrating integer,
    mdrating integer,
    dfrating integer,
    overall integer,
    tid integer NOT NULL
);


ALTER TABLE public.teams OWNER TO postgres;

--
-- Data for Name: games; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.games (date, location, leftteamscore, rightteamscore, gid) FROM stdin;
2000-01-01 10:00:00	Raymond James Stadium	4	4	565148679
2022-03-30 12:00:00	Wembley Stadium	2	3	291613511
2017-02-03 12:00:00	Old Trafford	4	3	776695127
\.


--
-- Data for Name: players; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.players (name, pace, shooting, passing, dribbling, defending, physicality, overall, pid) FROM stdin;
Nathan Bishop	92	63	77	100	90	75	83	1
Jack Butland	83	93	78	74	72	69	78	2
De Gea	66	80	81	76	86	79	78	3
Diogo Dalot	80	74	93	82	60	71	77	5
Tyler Fredricson	87	82	87	85	89	65	83	6
Phil Jones	90	62	100	89	66	66	79	7
Harry Maguire	60	80	65	88	94	92	80	9
Tyrell Malacia	88	61	64	61	78	74	71	10
Bruno Fernandes	79	92	67	88	79	87	82	11
Christian Eriksen	96	68	91	63	100	86	84	12
Johnquavious Johnson	87	78	66	75	76	73	76	13
Mickey	97	76	69	78	66	70	76	14
Jason Vorhees	62	62	81	86	86	92	78	15
\.


--
-- Data for Name: playsfor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.playsfor (pid, tid, "position") FROM stdin;
1	490275310	Defender
2	490275310	Defender
3	490275310	Goalkeeper
5	490275310	Defender
6	490275310	Midfielder
7	490275310	Midfielder
9	490275310	Midfielder
10	490275310	Attacker
11	490275310	Attacker
12	490275310	Attacker
13	490275310	Attacker
\.


--
-- Data for Name: teams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.teams (name, league, atkrating, mdrating, dfrating, overall, tid) FROM stdin;
Man City	Premier League	78	93	96	89	490275310
Manchester United	Premier League	90	88	79	86	364703652
\.


--
-- Name: games games_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (gid);


--
-- Name: players players_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_pkey PRIMARY KEY (pid);


--
-- Name: playsfor playsfor_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playsfor
    ADD CONSTRAINT playsfor_pk PRIMARY KEY (pid, tid);


--
-- Name: teams teams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (tid);


--
-- Name: teams unique_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT unique_name UNIQUE (name);


--
-- Name: playsfor playsfor_pid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playsfor
    ADD CONSTRAINT playsfor_pid_fkey FOREIGN KEY (pid) REFERENCES public.players(pid) ON DELETE CASCADE;


--
-- Name: playsfor playsfor_tid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playsfor
    ADD CONSTRAINT playsfor_tid_fkey FOREIGN KEY (tid) REFERENCES public.teams(tid);


--
-- PostgreSQL database dump complete
--

