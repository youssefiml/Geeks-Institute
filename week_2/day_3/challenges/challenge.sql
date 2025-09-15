-- Part 1:

-- 1)
create table Customer (
    id SERIAL primary key,
    first_name varchar(50) not null,
    last_name varchar(50) not null,
);
create table Customer_profile (
    id SERIAL primary key,
    isLoggedIn boolean not null default false,
    customer_id int not null,
   constraints fk_customer foreign key (customer_id) references Customer(id) on delete cascade

)

-- 2)
insert into Customer (first_name, last_name) values
('John', 'Doe'),
('Jerome', 'Lalu'),
('Lalu', 'Rive');

-- 3)
insert into Customer_profile (isLoggedIn, customer_id) values
((select true), (select id from Customer where first_name = 'John')),
((select false), (select id from Customer where first_name = 'Jerome')),

-- 4/1)
select c.first_name
from Customer c
join Customer_profile cp on c.id = cp.customer_id
where cp.isLoggedIn = true;

-- 4/2)
select c.first_name, coalesce(cp.isLoggedIn, false) as isLoggedIn
from Customer c
left join Customer_profile cp on c.id = cp.customer_id;

-- 4/3)
select count(*) from Customer c
left join Customer_profile cp on c.id = cp.customer_id
where coalesce(cp.isLoggedIn, false) = false;

-- Part 2:

-- 1)
create table Book (
    book_id SERIAL primary key,
    title varchar(100) not null,
    author varchar(100) not null
);

-- 2)
insert into Book (title, author) values
('Alice In Wonderland', 'Lewis Carroll'),
('Harry Potter', 'J.K Rowling'),
('To kill a mockingbird', 'Harper Lee');

-- 3)
create table Student (
    student_id SERIAL primary key,
    name varchar(100) not null unique,
    age int check (age <= 15)
);

-- 4)
 insert into Student (name, age) values
 ('John', 12),
 ('Lera', 11),
 ('Patrick', 10),
 ('Bob', 14);


-- 5)
create table Library (
    book_fk_id int not null,
    student_fk_id int not null,
    borrowed_date date default current_date,
    primary key (book_fk_id, student_fk_id),
    constraint fk_book foreign key (book_fk_id) references Book(book_id) on delete cascade on update cascade,
    constraint fk_student foreign key (student_fk_id) references Student(student_id) on delete cascade on update cascade
);

-- 6)
insert into Library (book_fk_id, student_fk_id, borrowed_date) values
((select book_id from Book where title = 'Alice In Wonderland'), (select student_id from Student where name = 'John'), '2022-02-15'),
((select book_id from Book where title = 'To kill a mockingbird'), (select student_id from Student where name = 'Bob'), '2021-03-03'),
((select book_id from Book where title = 'Alice In Wonderland'), (select student_id from Student where name = 'Lera'), '2021-05-23'),
((select book_id from Book where title = 'Harry Potter'), (select student_id from Student where name = 'Bob'), '2021-08-12');

-- 7/1)
select * from Library;

-- -- 7/2)
select s.name, b.title
from Library l
join Student s on l.student_fk_id = s.student_id
join Book b on l.book_fk_id = b.book_id;

-- 7/3)
select avg(s.age)
from Library l
join Student s on l.student_fk_id = s.student_id
join Book b on l.book_fk_id = b.book_id
where b.title = 'Alice In Wonderland';

-- 7/4)
delete from Student where name = 'John';