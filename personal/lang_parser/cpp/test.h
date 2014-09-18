#ifndef __TEST_HPP__
#define __TEST_HPP__

namespace ns {
	class foo{
		public:
			foo();
	};
}

class bar: ns::foo {
	public:
		bar();
};

#endif
